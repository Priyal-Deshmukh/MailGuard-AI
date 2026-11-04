# 🛡️ MailGuard AI
### Machine Learning-Based Spam Email Detection System

MailGuard AI is a web-based email security application that uses Machine Learning and Natural Language Processing (NLP) to classify emails as **Spam** or **Ham (Legitimate)**.

It combines a TF-IDF-based text processing pipeline, a Multinomial Naive Bayes classifier and Gmail API integration to provide automated email scanning through an interactive security dashboard.

## ✨ Features

- **Spam Detection:** Classifies email content as Spam or Ham.
- **Machine Learning:** Uses a trained Multinomial Naive Bayes classifier.
- **NLP Processing:** Applies TF-IDF for text feature extraction.
- **Manual Email Scanning:** Allows users to submit email content for classification.
- **Gmail Integration:** Connects to Gmail using OAuth 2.0 authentication.
- **Automated Email Scanning:** Fetches inbox emails and classifies their content.
- **Interactive Dashboard:** Displays email information and classification results.

## 🧠 Machine Learning Approach

The project follows a supervised machine learning approach.

| Stage | Technique |
|---|---|
| Dataset | Labeled email dataset |
| Text Processing | TF-IDF Vectorization |
| Stop Word Removal | English stop words |
| Feature Limit | 10,000 features |
| Train-Test Split | 80:20 |
| Classification Algorithm | Multinomial Naive Bayes |
| Saved Model | `spam_classifier.pkl` |

The model learns from labeled email examples and predicts whether new email content belongs to the Spam or Ham category.

## 🛠️ Technology Stack

- **Language:** Python
- **Backend:** Flask
- **Machine Learning:** Scikit-learn
- **NLP:** TF-IDF
- **Frontend:** HTML, CSS
- **Email Service:** Gmail API
- **Authentication:** OAuth 2.0
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
Spam-Email-Detection/
│
├── dataset/
│   └── emails.csv
│
├── models/
│   └── spam_classifier.pkl
│
├── src/
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── tests/
│
├── app.py
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd Spam-Email-Detection
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Flask secret key

```powershell
$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
```

### 7. Configure Gmail API

To use Gmail integration:

1. Create or select a project in Google Cloud Console.
2. Enable the Gmail API.
3. Configure the OAuth consent screen.
4. Create OAuth 2.0 client credentials for a Desktop or Web application, according to the application's configured OAuth flow.
5. Save the credentials file as `credentials.json` in the project root.
6. Complete the Gmail authorization process when prompted by the application.

The application uses OAuth authentication to access Gmail. The required redirect URI must match the URI configured in the application and Google Cloud Console.

### 8. Run the application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## 📧 How It Works

1. Open the MailGuard AI dashboard.
2. Enter email content for manual classification or connect your Gmail account.
3. Authenticate with Google when required.
4. Fetch inbox emails through the Gmail API.
5. The application processes the email content using TF-IDF.
6. The trained classifier predicts Spam or Ham.
7. View the classification results on the dashboard.

## 🔐 Security Notes

- Never upload `credentials.json`, `token.json` or `.env` files to a public repository.
- Keep your Flask secret key private.
- Use OAuth authentication for Gmail access.
- Grant only the required Gmail permissions.
- Do not publish personal email content or authentication tokens.

## 🚀 Future Improvements

- Advanced phishing detection.
- Suspicious URL analysis.
- Attachment security scanning.
- Deep learning-based classification.
- Improved model evaluation and analytics.
- Enhanced email security reporting.

## 📄 Project Documentation

For the detailed academic project report, refer to [`PROJECT_REPORT.md`](PROJECT_REPORT.md).

## 👩‍💻 Project Information

**Project Name:** MailGuard AI  
**Project Domain:** Artificial Intelligence and Machine Learning  
**Project Type:** Web-Based Application  
**Primary Objective:** Automated Spam Email Detection

---

*MailGuard AI — Making email communication smarter and safer through Machine Learning.*