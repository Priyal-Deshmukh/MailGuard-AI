# MailGuard AI
## Spam Email Detection System Using Machine Learning

### 1. Abstract

MailGuard AI is a machine learning-based email security application designed to identify spam and legitimate (ham) emails. It uses Natural Language Processing (NLP) techniques and a Multinomial Naive Bayes classifier to analyse email content and predict its category. The application also integrates with Gmail through the Gmail API and OAuth 2.0 authentication, allowing users to fetch inbox emails and scan them through the trained classification model.

### 2. Problem Statement

Email spam can expose users to unwanted messages, misleading content and potentially harmful links. Manually identifying spam emails can be time-consuming. Therefore, an automated system is required to analyse email content and distinguish spam messages from legitimate communication.

### 3. Objectives

- Develop an automated spam email classification system.
- Apply NLP techniques to process email text.
- Train a machine learning model to classify emails as Spam or Ham.
- Integrate Gmail to retrieve emails for automated scanning.
- Provide an interactive dashboard to display classification results.

### 4. Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Machine Learning | Scikit-learn |
| NLP and Feature Extraction | TF-IDF |
| Classification Algorithm | Multinomial Naive Bayes |
| Email Integration | Gmail API |
| Authentication | OAuth 2.0 |
| Frontend | HTML, CSS |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |

### 5. Dataset Description

The project uses an email dataset stored in `dataset/emails.csv`.

The dataset contains email text and corresponding labels. These labels represent two categories:

- **Spam:** Unwanted or unsolicited email.
- **Ham:** Legitimate email.

The dataset is used to train and evaluate the machine learning classifier.

### 6. Methodology

The system follows these steps:

1. **Data Loading:** The email dataset is loaded using Python.
2. **Data Preparation:** Email text and corresponding labels are separated for model training.
3. **Data Splitting:** The dataset is divided into training and testing sets using an 80:20 split, with stratification and a fixed random state.
4. **Text Vectorization:** TF-IDF (Term Frequency–Inverse Document Frequency) converts email text into numerical features. The vectorizer uses English stop-word removal and a maximum of 10,000 features.
5. **Model Training:** A Multinomial Naive Bayes classifier is trained using the extracted features.
6. **Model Saving:** The trained classifier is saved as `spam_classifier.pkl` for use in the Flask application.
7. **Prediction:** New email content is processed and classified as Spam or Ham.

### 7. System Architecture

The application consists of four main components:

- **Frontend:** Provides the user interface for scanning emails and viewing results.
- **Flask Backend:** Handles user requests, email processing and model predictions.
- **Machine Learning Model:** Analyses vectorized email text and generates classifications.
- **Gmail Integration:** Uses OAuth 2.0 and the Gmail API to retrieve inbox messages for scanning.

### 8. Implementation

MailGuard AI provides two main ways to analyse emails:

**A. Manual Email Scanning**

Users can enter email content into the dashboard. The Flask backend processes the text using the trained model and displays the predicted category.

**B. Gmail Email Scanning**

Users can authenticate their Gmail account using OAuth 2.0. The application retrieves inbox messages through the Gmail API, extracts relevant email information and classifies each message using the trained model.

The dashboard presents email details and their corresponding Spam or Ham classifications.

### 9. Key Features

- Machine learning-based spam detection.
- NLP-based text feature extraction.
- Manual email content scanning.
- Gmail account integration.
- Automated inbox email classification.
- Interactive security dashboard.
- Separate Spam and Ham result views.

### 10. Testing and Results

The application has been tested locally for its main functionalities, including dashboard access, manual email classification and Gmail email retrieval and scanning.

The trained model generates Spam or Ham predictions for the processed email content.

Quantitative evaluation metrics such as accuracy, precision, recall and F1-score should be included after verification from the actual model evaluation output.

### 11. Limitations

- Classification depends on the quality and representation of the training dataset.
- Predictions may not always be correct for unusual or previously unseen email content.
- Gmail integration requires valid OAuth authentication and API access.
- The system currently focuses on email text classification rather than complete malicious-link or attachment analysis.

### 12. Future Scope

- Improve classification performance using larger and more diverse datasets.
- Introduce advanced NLP and deep learning techniques.
- Add phishing URL and suspicious attachment detection.
- Provide more detailed email security analytics.
- Improve classification evaluation and monitoring.

### 13. Conclusion

MailGuard AI demonstrates the practical application of machine learning and Natural Language Processing in email security. By combining a TF-IDF-based text processing pipeline, a Multinomial Naive Bayes classifier, Flask and Gmail API integration, the system provides an automated approach to identifying spam and legitimate emails through a user-friendly dashboard.

The project demonstrates how machine learning can be integrated into a real-world web application to address a common digital communication problem.

---

**Project:** MailGuard AI  
**Domain:** Artificial Intelligence and Machine Learning  
**Application Type:** Web-Based Email Spam Detection System