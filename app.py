
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import joblib
import os
import base64
import re
import html

# Local development only.
# Remove this setting when deploying with HTTPS.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError


# --------------------------------------------------
# 1. FLASK APPLICATION CONFIGURATION
# --------------------------------------------------

app = Flask(__name__)
@app.before_request
def log_requests():
    print(
        f"[REQUEST] {request.method} {request.path}",
        flush=True
    )

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "FLASK_SECRET_KEY environment variable is not set."
    )


# --------------------------------------------------
# 2. MACHINE LEARNING MODEL
# --------------------------------------------------

model = joblib.load("models/spam_classifier.pkl")


# --------------------------------------------------
# 3. GMAIL OAUTH CONFIGURATION
# --------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

CLIENT_SECRET_FILE = "credentials.json"
TOKEN_FILE = "token.json"

REDIRECT_URI = "http://127.0.0.1:5000/oauth2callback"


# --------------------------------------------------
# 4. LOAD GMAIL CREDENTIALS
# --------------------------------------------------

def get_gmail_credentials():

    if not os.path.exists(TOKEN_FILE):
        return None

    credentials = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        SCOPES
    )

    if credentials.expired and credentials.refresh_token:

        credentials.refresh(Request())

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    if credentials.valid:
        return credentials

    return None


# --------------------------------------------------
# 5. CONNECT TO GMAIL
# --------------------------------------------------

@app.route("/connect-gmail")
def connect_gmail():

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        autogenerate_code_verifier=True
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    session["oauth_state"] = state
    session["oauth_code_verifier"] = flow.code_verifier

    return redirect(authorization_url)

# --------------------------------------------------
# 6. GOOGLE OAUTH CALLBACK
# --------------------------------------------------

@app.route("/oauth2callback")
def oauth2callback():

    print("========== OAUTH CALLBACK REACHED ==========", flush=True)
    print("Query parameters received:", list(request.args.keys()), flush=True)

    state = session.get("oauth_state")
    code_verifier = session.get("oauth_code_verifier")

    print("OAuth state present:", bool(state), flush=True)
    print("Code verifier present:", bool(code_verifier), flush=True)

    if not state or not code_verifier:
        session.pop("oauth_state", None)
        session.pop("oauth_code_verifier", None)

        return (
            "OAuth session expired. Please connect Gmail again.",
            400
        )

    if request.args.get("error"):
        session.pop("oauth_state", None)
        session.pop("oauth_code_verifier", None)

        return (
            "Google authorization was not completed. "
            "Please try connecting Gmail again.",
            400
        )

    try:

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=SCOPES,
            state=state,
            redirect_uri=REDIRECT_URI,
            autogenerate_code_verifier=True
        )

        # Restore the original verifier generated during connection.
        flow.code_verifier = code_verifier

        flow.fetch_token(
            authorization_response=request.url
        )

        credentials = flow.credentials

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

        session.pop("oauth_state", None)
        session.pop("oauth_code_verifier", None)

        print("Gmail authorization successful!", flush=True)

        return redirect(url_for("home"))

    except Exception:

        app.logger.exception(
            "Google OAuth callback failed"
        )

        session.pop("oauth_state", None)
        session.pop("oauth_code_verifier", None)

        return (
            "Unable to complete Gmail authorization. "
            "Please try again.",
            400
        )


# --------------------------------------------------
# 7. DECODE EMAIL CONTENT
# --------------------------------------------------

def decode_email_data(data):

    if not data:
        return ""

    decoded = base64.urlsafe_b64decode(
        data + "=" * (-len(data) % 4)
    )

    return decoded.decode(
        "utf-8",
        errors="replace"
    )


# --------------------------------------------------
# 8. EXTRACT EMAIL BODY
# --------------------------------------------------

def extract_email_body(payload):

    mime_type = payload.get("mimeType", "")

    # Plain text email
    if mime_type == "text/plain":

        data = payload.get(
            "body", {}
        ).get("data")

        return decode_email_data(data)

    # HTML email
    if mime_type == "text/html":

        data = payload.get(
            "body", {}
        ).get("data")

        html_content = decode_email_data(data)

        text_content = re.sub(
            r"<[^>]+>",
            " ",
            html_content
        )

        return html.unescape(text_content)

    # Multipart email
    parts = payload.get("parts", [])

    # Prefer plain text to avoid duplicate HTML/plain-text content
    for part in parts:

        if part.get("mimeType") == "text/plain":

            body = extract_email_body(part)

            if body:
                return body

    # If no plain-text part exists, use HTML
    for part in parts:

        if part.get("mimeType") == "text/html":

            body = extract_email_body(part)

            if body:
                return body

    # Handle nested multipart messages
    body_text = ""

    for part in parts:

        if part.get("mimeType", "").startswith("multipart/"):

            body_text += extract_email_body(part) + "\n"

    return body_text


# --------------------------------------------------
# 9. FETCH AND CLASSIFY GMAIL MESSAGES
# --------------------------------------------------

def fetch_and_classify_emails():

    credentials = get_gmail_credentials()

    if not credentials:

        raise RuntimeError(
            "Gmail authorization is unavailable. "
            "Please reconnect Gmail."
        )

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    response = service.users().messages().list(
        userId="me",
        maxResults=10,
        q="in:inbox"
    ).execute()

    messages = response.get("messages", [])

    classified_emails = []

    for message in messages:

        email_data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        payload = email_data.get(
            "payload", {}
        )

        headers = payload.get(
            "headers", []
        )

        header_dict = {
            header["name"].lower(): header["value"]
            for header in headers
        }

        sender = header_dict.get(
            "from",
            "Unknown sender"
        )

        subject = header_dict.get(
            "subject",
            "No subject"
        )

        date = header_dict.get(
            "date",
            ""
        )

        body = extract_email_body(payload)

        email_text = (
            "Subject: " + subject + "\n"
            "From: " + sender + "\n"
            + body
        )

        prediction = model.predict(
            [email_text]
        )[0]

        classified_emails.append({

            "sender": sender,

            "subject": subject,

            "date": date,

            "body": body[:500],

            "prediction": prediction.upper()

        })

    return classified_emails


# --------------------------------------------------
# 10. DISCONNECT GMAIL
# --------------------------------------------------

@app.route("/disconnect-gmail")
def disconnect_gmail():

    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)

    session.pop("oauth_state", None)

    return redirect(url_for("home"))


# --------------------------------------------------
# 11. MAIN DASHBOARD
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    email_text = ""

    gmail_connected = False
    gmail_emails = []
    gmail_error = None

    # Check Gmail connection
    try:

        credentials = get_gmail_credentials()

        if credentials:
            gmail_connected = True

    except Exception:

        app.logger.exception(
            "Unable to load Gmail credentials"
        )

        gmail_error = (
            "Gmail authorization expired or is unavailable. "
            "Please reconnect Gmail."
        )

    # Manual email classification
    if request.method == "POST":

        email_text = request.form.get(
            "email",
            ""
        ).strip()

        if email_text:

            prediction = model.predict(
                [email_text]
            )[0]

            result = (
                "SPAM"
                if prediction == "spam"
                else "HAM"
            )

    # Fetch Gmail only when requested
    if (
        gmail_connected
        and request.method == "GET"
        and request.args.get("fetch") == "1"
    ):

        try:

            gmail_emails = (
                fetch_and_classify_emails() or []
            )

        except HttpError:

            app.logger.exception(
                "Gmail API request failed"
            )

            gmail_error = (
                "Gmail API request failed. "
                "Please try again."
            )

        except Exception:

            app.logger.exception(
                "Unable to fetch Gmail messages"
            )

            gmail_error = (
                "Unable to fetch emails. "
                "Please reconnect Gmail and try again."
            )

    return render_template(
        "index.html",
        result=result,
        email_text=email_text,
        gmail_connected=gmail_connected,
        gmail_emails=gmail_emails,
        gmail_error=gmail_error
    )


# --------------------------------------------------
# 12. RUN APPLICATION
# --------------------------------------------------
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )
