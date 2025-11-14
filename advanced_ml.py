import re
import pickle
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline

class AdvancedMLModel:
    def __init__(self):
        self.pipeline = None
        self.is_trained = False
        self.feature_names = []
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        
    def preprocess_text(self, text):
        """Clean and preprocess text data"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def extract_features(self, email_features):
        """Extract comprehensive features from email"""
        subject = self.preprocess_text(email_features.get('subject', ''))
        body = self.preprocess_text(email_features.get('body', ''))
        
        # Combine subject and body
        combined_text = f"{subject} {body}"
        
        # Additional numerical features
        features = {
            'text': combined_text,
            'subject_length': len(subject),
            'body_length': len(body),
            'has_urgent': 1 if any(word in subject.lower() or word in body.lower() 
                                 for word in ['urgent', 'immediate', 'asap', 'now']) else 0,
            'has_verify': 1 if any(word in subject.lower() or word in body.lower() 
                                 for word in ['verify', 'confirm', 'authenticate']) else 0,
            'has_login': 1 if any(word in subject.lower() or word in body.lower() 
                                for word in ['login', 'password', 'account', 'security']) else 0,
            'caps_ratio': sum(1 for c in body if c.isupper()) / len(body) if body else 0,
            'exclamation_count': body.count('!'),
            'question_count': body.count('?'),
            'link_count': len(email_features.get('links', []))
        }
        
        return features
    
    def train(self, training_data):
        """Train the advanced ML model"""
        texts = []
        labels = []
        
        for email_features, label in training_data:  # Fixed: was training_
            features = self.extract_features(email_features)
            texts.append(features['text'])
            labels.append(label)
        
        # Create pipeline
        self.pipeline = Pipeline([
            ('tfidf', self.vectorizer),
            ('classifier', self.classifier)
        ])
        
        # Train the pipeline
        self.pipeline.fit(texts, labels)
        self.is_trained = True
        
        print("Advanced ML Model trained successfully!")
        return True
    
    def predict(self, email_features):
        """Predict if email is phishing using advanced model"""
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        features = self.extract_features(email_features)
        text = features['text']
        
        # Make prediction
        prediction = self.pipeline.predict([text])[0]
        probability = self.pipeline.predict_proba([text])[0]
        
        # Get the confidence score (probability of the predicted class)
        confidence = max(probability)
        
        return prediction, confidence
    
    def evaluate(self, test_data):
        """Evaluate model performance"""
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        texts = []
        true_labels = []
        
        for email_features, label in test_data:  # Fixed: was test_
            features = self.extract_features(email_features)
            texts.append(features['text'])
            true_labels.append(label)
        
        predictions = self.pipeline.predict(texts)
        
        accuracy = accuracy_score(true_labels, predictions)
        precision = precision_score(true_labels, predictions, zero_division=0)
        recall = recall_score(true_labels, predictions, zero_division=0)
        f1 = f1_score(true_labels, predictions, zero_division=0)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    
    def save_model(self, filepath):
        """Save the trained model"""
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        model_data = {
            'pipeline': self.pipeline,
            'is_trained': self.is_trained
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a pre-trained model"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.pipeline = model_data['pipeline']
        self.is_trained = model_data['is_trained']
        print(f"Model loaded from {filepath}")

# Test function
def test_advanced_ml():
    # Create sample training data
    training_data = [
        ({
            'subject': 'Meeting Reminder',
            'body': 'Hi, just a reminder about our meeting tomorrow at 2 PM. Looking forward to seeing you there.',
            'from_address': 'colleague@company.com',
            'to_address': 'user@company.com',
            'reply_to': '',
            'links': [],
            'attachments': 0,
            'sender_domain': 'company.com',
            'reply_domain': ''
        }, 0),  # Legitimate
        
        ({
            'subject': 'URGENT: Account Security Alert',
            'body': 'Dear Customer, Your account has been suspended. Please click here to verify: http://fake-bank-login.com/verify Click now to secure your account!',
            'from_address': 'fake-bank@example.com',
            'to_address': 'victim@gmail.com',
            'reply_to': 'security@fake-bank.com',
            'links': ['http://fake-bank-login.com/verify'],
            'attachments': 0,
            'sender_domain': 'example.com',
            'reply_domain': 'fake-bank.com'
        }, 1),  # Phishing
        
        ({
            'subject': 'Password Reset Required',
            'body': 'Your password needs to be reset immediately. Click here: https://secure-company-login.com/reset',
            'from_address': 'admin@company.com',
            'to_address': 'user@company.com',
            'reply_to': '',
            'links': ['https://secure-company-login.com/reset'],
            'attachments': 0,
            'sender_domain': 'company.com',
            'reply_domain': ''
        }, 1),  # Phishing
        
        ({
            'subject': 'Weekly Report',
            'body': 'Please find attached the weekly sales report. Let me know if you have any questions.',
            'from_address': 'manager@company.com',
            'to_address': 'employee@company.com',
            'reply_to': '',
            'links': [],
            'attachments': 1,
            'sender_domain': 'company.com',
            'reply_domain': ''
        }, 0)   # Legitimate
    ]
    
    ml_model = AdvancedMLModel()
    ml_model.train(training_data)
    
    # Test prediction
    test_features = {
        'subject': 'URGENT: Account Security Alert',
        'body': 'Dear Customer, Your account has been suspended. Please click here to verify: http://fake-bank-login.com/verify Click now to secure your account!',
        'from_address': 'fake-bank@example.com',
        'to_address': 'victim@gmail.com',
        'reply_to': 'security@fake-bank.com',
        'links': ['http://fake-bank-login.com/verify'],
        'attachments': 0,
        'sender_domain': 'example.com',
        'reply_domain': 'fake-bank.com'
    }
    
    prediction, confidence = ml_model.predict(test_features)
    
    print("=== Advanced ML Model Test Results ===")
    print(f"Prediction: {prediction} (1=Phishing, 0=Legitimate)")
    print(f"Confidence: {confidence:.2f}")
    
    # Evaluate model
    evaluation = ml_model.evaluate(training_data)  # Use training_data for evaluation in this test
    print("Evaluation Metrics:")
    for metric, value in evaluation.items():
        print(f"  {metric}: {value:.3f}")
    
    return prediction, confidence

if __name__ == "__main__":
    test_advanced_ml()