
import csv
from pathlib import Path
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser


# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
OUTPUT_FILE = DATASET_DIR / "emails.csv"


class HTMLTextExtractor(HTMLParser):
    """Extract readable text from HTML emails."""

    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_data(self, data):
        self.text_parts.append(data)

    def get_text(self):
        return " ".join(self.text_parts)


def extract_email_text(file_path):
    """Extract subject and message body from an email."""

    with open(file_path, "rb") as file:
        message = BytesParser(policy=policy.default).parse(file)

    subject = str(message.get("subject", ""))

    plain_parts = []
    html_parts = []

    for part in message.walk():

        if part.get_content_disposition() == "attachment":
            continue

        if part.get_content_type() == "text/plain":
            try:
                content = part.get_content()
                if isinstance(content, str):
                    plain_parts.append(content)
            except Exception:
                continue

        elif part.get_content_type() == "text/html":
            try:
                content = part.get_content()
                if isinstance(content, str):
                    html_parts.append(content)
            except Exception:
                continue

    # Prefer plain text; use HTML only if plain text is unavailable
    if plain_parts:
        body = " ".join(plain_parts)
    else:
        extractor = HTMLTextExtractor()
        for html in html_parts:
            extractor.feed(html)
        body = extractor.get_text()

    return subject + " " + body


def load_emails(folder_name, label):
    """Read all emails from a folder."""

    folder = DATASET_DIR / folder_name
    emails = []

    for file_path in folder.iterdir():

        # Ignore metadata and other non-email files
        if not file_path.is_file() or file_path.name.lower() == "cmds":
            continue

        try:
            text = extract_email_text(file_path)

            if text.strip():
                emails.append({
                    "text": text,
                    "label": label
                })

        except Exception as error:
            print(f"Could not read {file_path.name}: {error}")

    print(f"{label.upper()} emails processed: {len(emails)}")
    return emails


def main():
    print("Reading email dataset...")

    ham_emails = load_emails("easy_ham_2", "ham")
    spam_emails = load_emails("spam_2", "spam")

    all_emails = ham_emails + spam_emails

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["text", "label"]
        )

        writer.writeheader()
        writer.writerows(all_emails)

    print("\nDataset preparation completed!")
    print(f"Total emails saved: {len(all_emails)}")
    print(f"CSV location: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
