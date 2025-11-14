import re
from collections import Counter, defaultdict
import pickle

class MLModel:
    def __init__(self):
        self.vocabulary = set()
        self.phishing_words = Counter()
        self.legitimate_words = Counter()
        self.is_trained = False
        self.total_phishing_emails = 0
        self.total_legitimate_emails = 0
    
    def preprocess_text(self, text):
        """Clean and preprocess text data"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def extract_features(self, email_features):
        """Extract ML features from email"""
        subject = self.preprocess_text(email_features.get('subject', ''))
        body = self.preprocess_text(email_features.get('body', ''))
        
        # Combine subject and body for feature extraction
        combined_text = f"{subject} {body}"
        
        # Split into words
        words = combined_text.split()
        
        return words
    
    def train(self, training_data):
        """Train the ML model using a simple Naive Bayes approach"""
        for email_features, label in training_data:
            words = self.extract_features(email_features)
            
            if label == 1:  # Phishing
                self.total_phishing_emails += 1
                for word in words:
                    self.phishing_words[word] += 1
                    self.vocabulary.add(word)
            else:  # Legitimate
                self.total_legitimate_emails += 1
                for word in words:
                    self.legitimate_words[word] += 1
                    self.vocabulary.add(word)
        
        self.is_trained = True
        print("ML Model trained successfully!")
    
    def predict(self, email_features):
        """Predict if email is phishing using Naive Bayes"""
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        words = self.extract_features(email_features)
        
        # Calculate prior probabilities
        total_emails = self.total_phishing_emails + self.total_legitimate_emails
        if total_emails == 0:
            return 0, 0.5  # Default to legitimate if no training data
            
        phishing_prob = self.total_phishing_emails / total_emails
        legitimate_prob = self.total_legitimate_emails / total_emails
        
        # Calculate word probabilities for phishing and legitimate
        phishing_word_prob = 1.0
        legitimate_word_prob = 1.0
        
        for word in words:
            # Laplace smoothing to handle unseen words
            phishing_word_count = self.phishing_words.get(word, 0)
            legitimate_word_count = self.legitimate_words.get(word, 0)
            
            # Calculate conditional probabilities
            total_phishing_words = sum(self.phishing_words.values())
            total_legitimate_words = sum(self.legitimate_words.values())
            
            # Add 1 for Laplace smoothing
            phishing_cond_prob = (phishing_word_count + 1) / (total_phishing_words + len(self.vocabulary))
            legitimate_cond_prob = (legitimate_word_count + 1) / (total_legitimate_words + len(self.vocabulary))
            
            phishing_word_prob *= phishing_cond_prob
            legitimate_word_prob *= legitimate_cond_prob
        
        # Final probabilities
        final_phishing_prob = phishing_prob * phishing_word_prob
        final_legitimate_prob = legitimate_prob * legitimate_word_prob
        
        # Determine prediction
        if final_phishing_prob > final_legitimate_prob:
            prediction = 1
            confidence = final_phishing_prob / (final_phishing_prob + final_legitimate_prob)
        else:
            prediction = 0
            confidence = final_legitimate_prob / (final_phishing_prob + final_legitimate_prob)
        
        return prediction, confidence
    
    def save_model(self, filepath):
        """Save the trained model"""
        model_data = {
            'vocabulary': self.vocabulary,
            'phishing_words': self.phishing_words,
            'legitimate_words': self.legitimate_words,
            'total_phishing_emails': self.total_phishing_emails,
            'total_legitimate_emails': self.total_legitimate_emails,
            'is_trained': self.is_trained
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """Load a pre-trained model"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vocabulary = model_data['vocabulary']
        self.phishing_words = model_data['phishing_words']
        self.legitimate_words = model_data['legitimate_words']
        self.total_phishing_emails = model_data['total_phishing_emails']
        self.total_legitimate_emails = model_data['total_legitimate_emails']
        self.is_trained = model_data['is_trained']

# Test function
def test_ml_model():
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
        }, 0),  # 0 = legitimate
        
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
        }, 1),  # 1 = phishing
        
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
        }, 1),  # 1 = phishing
        
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
        }, 0)   # 0 = legitimate
    ]
    
    ml_model = MLModel()
    ml_model.train(training_data)
    
    # Test prediction on a new email
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
    
    print("=== ML Model Test Results ===")
    print(f"Prediction: {prediction} (1=Phishing, 0=Legitimate)")
    print(f"Confidence: {confidence:.2f}")
    
    return prediction, confidence

if __name__ == "__main__":
    test_ml_model()