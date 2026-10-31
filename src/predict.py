
import joblib

# Load the trained machine learning model
model = joblib.load("models/spam_classifier.pkl")

print("================================")
print("       SPAM EMAIL DETECTOR")
print("================================")

# Take email text from the user
email_text = input("\nEnter your email text:\n")

# Predict the email category
prediction = model.predict([email_text])[0]

# Display the result
print("\nPrediction:")

if prediction == "spam":
    print("WARNING: This email is SPAM!")
else:
    print("This email appears to be HAM (NOT SPAM).")

print("================================")

