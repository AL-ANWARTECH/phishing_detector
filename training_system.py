import os
import json
import random
from datetime import datetime
from advanced_ml import AdvancedMLModel
from phishing_detector import PhishingDetector
from logger import get_logger
from config import Config

class TrainingSystem:
    def __init__(self):
        self.logger = get_logger()
        self.config = Config()
        self.advanced_model = AdvancedMLModel()
        self.phishing_detector = PhishingDetector()
    
    def load_sample_data(self):
        """Load sample training data for demonstration"""
        sample_data = [
            # Legitimate emails
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
                'subject': 'Project Update',
                'body': 'Here is the weekly project update. Please review the attached document.',
                'from_address': 'manager@company.com',
                'to_address': 'team@company.com',
                'reply_to': '',
                'links': [],
                'attachments': 1,
                'sender_domain': 'company.com',
                'reply_domain': ''
            }, 0),  # Legitimate
            
            ({
                'subject': 'Welcome to Our Newsletter',
                'body': 'Thank you for subscribing to our newsletter. Here are this week\'s updates.',
                'from_address': 'newsletter@company.com',
                'to_address': 'subscriber@user.com',
                'reply_to': '',
                'links': ['http://company.com/news'],
                'attachments': 0,
                'sender_domain': 'company.com',
                'reply_domain': ''
            }, 0),  # Legitimate
            
            # Phishing emails
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
                'subject': 'Verify Your PayPal Account Now!',
                'body': 'Your PayPal account will be suspended in 24 hours. Click here to verify immediately: http://paypal-verify-fake.com',
                'from_address': 'paypal-security@fake.com',
                'to_address': 'user@paypal.com',
                'reply_to': 'verify@paypal-fake.com',
                'links': ['http://paypal-verify-fake.com'],
                'attachments': 0,
                'sender_domain': 'fake.com',
                'reply_domain': 'paypal-fake.com'
            }, 1),  # Phishing
            
            ({
                'subject': 'Password Reset Required - Immediate Action Needed',
                'body': 'Your password has been compromised. Reset it now by clicking: https://secure-login-fake.com/reset',
                'from_address': 'admin@fake-security.com',
                'to_address': 'user@company.com',
                'reply_to': '',
                'links': ['https://secure-login-fake.com/reset'],
                'attachments': 0,
                'sender_domain': 'fake-security.com',
                'reply_domain': ''
            }, 1),  # Phishing
        ]
        return sample_data
    
    def generate_training_data(self, size=100):
        """Generate larger training dataset for demonstration"""
        base_data = self.load_sample_data()
        generated_data = []
        
        # Expand the base dataset
        for i in range(size):
            # Randomly select a base sample
            base_sample = random.choice(base_data)
            email_features, label = base_sample
            
            # Create variations to expand dataset
            new_features = email_features.copy()
            
            # Add some random variations
            if label == 0:  # Legitimate
                subjects = [
                    f"Meeting reminder #{i}",
                    f"Project update #{i}",
                    f"Weekly report #{i}",
                    f"Newsletter #{i}",
                    f"Task assignment #{i}"
                ]
                new_features['subject'] = random.choice(subjects)
            else:  # Phishing
                subjects = [
                    f"URGENT: Security Alert #{i}",
                    f"Verify Account #{i}",
                    f"Password Reset Required #{i}",
                    f"Account Suspended #{i}",
                    f"Immediate Action Required #{i}"
                ]
                new_features['subject'] = random.choice(subjects)
            
            generated_data.append((new_features, label))
        
        self.logger.info(f"Generated {len(generated_data)} training samples")
        return generated_data
    
    def train_advanced_model(self, training_data=None):
        """Train the advanced ML model"""
        if training_data is None:
            training_data = self.load_sample_data()
        
        self.logger.info(f"Starting advanced model training with {len(training_data)} samples")
        
        try:
            success = self.advanced_model.train(training_data)
            if success:
                # Save the trained model
                model_path = os.path.join(self.config.MODEL_PATH)
                model_dir = os.path.dirname(model_path)
                if model_dir and not os.path.exists(model_dir):
                    os.makedirs(model_dir)
                
                self.advanced_model.save_model(model_path)
                self.logger.info(f"Advanced model trained and saved to {model_path}")
            return success
        except Exception as e:
            self.logger.error(f"Error training advanced model: {str(e)}")
            return False
    
    def evaluate_model(self, test_data=None):
        """Evaluate the trained model"""
        if test_data is None:
            test_data = self.load_sample_data()
        
        if not self.advanced_model.is_trained:
            self.logger.warning("Model not trained, training first...")
            self.train_advanced_model(test_data)
        
        try:
            evaluation = self.advanced_model.evaluate(test_data)
            self.logger.info("Model evaluation completed")
            
            print("=== Model Evaluation Results ===")
            for metric, value in evaluation.items():
                print(f"{metric}: {value:.3f}")
            
            return evaluation
        except Exception as e:
            self.logger.error(f"Error evaluating model: {str(e)}")
            return None
    
    def test_detection_accuracy(self, test_data=None):
        """Test the overall detection accuracy"""
        if test_data is None:
            test_data = self.load_sample_data()
        
        correct_predictions = 0
        total_tests = len(test_data)
        
        for email_features, true_label in test_data:
            # Convert features to email content format for testing
            email_content = f"""From: {email_features['from_address']}
To: {email_features['to_address']}
Subject: {email_features['subject']}

{email_features['body']}
"""
            
            # Analyze with our phishing detector
            result = self.phishing_detector.analyze_email(email_content)
            predicted_label = 1 if result['is_phishing'] else 0
            
            if predicted_label == true_label:
                correct_predictions += 1
        
        accuracy = correct_predictions / total_tests if total_tests > 0 else 0
        
        print(f"=== Detection Accuracy Test ===")
        print(f"Correct predictions: {correct_predictions}/{total_tests}")
        print(f"Accuracy: {accuracy:.3f}")
        
        return accuracy
    
    def save_training_data(self, training_data, filename='training_data.json'):
        """Save training data to file"""
        try:
            # Convert to serializable format
            serializable_data = []
            for features, label in training_data:
                serializable_data.append((features, label))
            
            with open(filename, 'w') as f:
                json.dump(serializable_data, f, indent=2)
            
            self.logger.info(f"Training data saved to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving training data: {str(e)}")
            return False
    
    def load_training_data(self, filename='training_data.json'):
        """Load training data from file"""
        try:
            with open(filename, 'r') as f:
                training_data = json.load(f)
            
            # Convert back to the expected format
            converted_data = []
            for features, label in training_data:
                converted_data.append((features, label))
            
            self.logger.info(f"Training data loaded from {filename}")
            return converted_data
        except Exception as e:
            self.logger.error(f"Error loading training data: {str(e)}")
            return None

# Test function
def test_training_system():
    print("=== Training System Test ===")
    
    training_system = TrainingSystem()
    
    # Load sample data
    sample_data = training_system.load_sample_data()
    print(f"Loaded {len(sample_data)} sample data points")
    
    # Generate larger training dataset
    large_dataset = training_system.generate_training_data(size=20)
    print(f"Generated larger dataset with {len(large_dataset)} samples")
    
    # Train the advanced model
    training_system.train_advanced_model(large_dataset)
    
    # Evaluate the model
    evaluation = training_system.evaluate_model(sample_data)
    
    # Test detection accuracy
    accuracy = training_system.test_detection_accuracy(sample_data)
    
    # Save training data
    training_system.save_training_data(large_dataset)
    
    print("\nTraining system test completed successfully!")

if __name__ == "__main__":
    test_training_system()