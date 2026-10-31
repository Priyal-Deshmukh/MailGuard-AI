# MailGuard-AI

A machine learning web app that detects spam and legitimate (ham) emails, with optional Gmail integration to scan your inbox.

![Dashboard screenshot](screenshots/dashboard.png)

## Features
- Paste any email and get an instant SPAM / HAM prediction
- Connect Gmail (read-only) and classify your 10 most recent inbox emails
- Dashboard with model accuracy, precision/recall/F1 and confusion matrix

## Model performance
| Metric | Value |
|---|---|
| Algorithm | Multinomial Naive Bayes |
| Features | TF-IDF |
| Test accuracy | 98.21% (550 / 560 correct) |

Confusion matrix on 560 test emails:

| | Predicted HAM | Predicted SPAM |
|---|---|---|
| Actual HAM | 277 | 3 |
| Actual SPAM | 7 | 273 |

## Tech stack
Python, Flask, scikit-learn, joblib, Google Gmail API (OAuth 2.0), HTML/CSS

## Project structure
```
Spam-Email-Detection/
├── app.py               # Flask app and Gmail integration
├── dataset/             # Training emails
├── models/              # Trained spam_classifier.pkl
├── src/
│   ├── prepare_dataset.py
│   ├── train_model.py
│   └── predict.py
├── static/style.css
├── templates/index.html
└── requirements.txt
```

## Setup
1. Clone the repo and create a virtual environment:
   ```
   git clone https://github.com/Priyal-Deshmukh/MailGuard-AI.git
   cd MailGuard-AI
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. (Optional, for Gmail) Create OAuth credentials in Google Cloud Console, enable the Gmail API, download the file as `credentials.json` into the project root, and add `http://127.0.0.1:5000/oauth2callback` as a redirect URI.
3. Set a secret key and run:
   ```
   $env:FLASK_SECRET_KEY="your-random-secret"
   python app.py
   ```
4. Open http://127.0.0.1:5000

## Privacy
Gmail access is read-only (`gmail.readonly`). Emails are classified locally and are not stored.

## Limitations and future scope
- Single shared Gmail token (per-user login needed for production)
- Compare with logistic regression / transformer models
- Phishing link detection
- Move detected spam to the Spam folder

## Author
Priyal Deshmukh