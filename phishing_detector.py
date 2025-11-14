from email_parser import EmailParser
from rule_engine import RuleEngine
from ml_model import MLModel
from url_analyzer import URLAnalyzer  # Add this import
from config import Config

class PhishingDetector:
    def __init__(self):
        self.email_parser = EmailParser()
        self.rule_engine = RuleEngine()
        self.ml_model = MLModel()
        self.url_analyzer = URLAnalyzer()  # Add URL analyzer
        self.config = Config()
    
    def analyze_email(self, email_content):
        """Analyze email for phishing indicators"""
        try:
            # Parse the email
            features = self.email_parser.parse_email(email_content)
            
            # Get rule-based score
            rule_score, rule_reasons = self.rule_engine.evaluate_rules(features)
            
            # Get ML-based prediction
            ml_prediction, ml_confidence = 0, 0.5  # Default values
            if self.ml_model.is_trained:
                ml_prediction, ml_confidence = self.ml_model.predict(features)
            
            # Get URL analysis
            url_score, url_reasons = self.url_analyzer.analyze_email_urls(features)
            
            # Calculate hybrid score with URL analysis
            hybrid_score = self.calculate_enhanced_hybrid_score(
                rule_score, ml_prediction, ml_confidence, url_score
            )
            
            # Determine if phishing
            is_phishing = hybrid_score > self.config.PHISHING_THRESHOLD
            
            result = {
                'is_phishing': is_phishing,
                'confidence_score': hybrid_score,
                'rule_score': rule_score,
                'ml_prediction': ml_prediction,
                'ml_confidence': ml_confidence,
                'url_score': url_score,
                'rule_reasons': rule_reasons,
                'url_reasons': url_reasons,
                'features': features
            }
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'is_phishing': False,
                'confidence_score': 0
            }
    
    def calculate_enhanced_hybrid_score(self, rule_score, ml_prediction, ml_confidence, url_score):
        """Calculate hybrid score with URL analysis"""
        # Normalize scores to 0-1 range
        normalized_rule_score = rule_score / 100.0
        normalized_url_score = url_score / 100.0
        
        # ML prediction contributes based on confidence
        ml_contribution = ml_prediction * ml_confidence
        
        # Weighted combination with URL score
        hybrid_score = (
            (self.config.RULE_WEIGHT * 0.6 * normalized_rule_score * 100) +
            (self.config.ML_WEIGHT * 0.6 * ml_contribution * 100) +
            (0.4 * normalized_url_score * 100)  # URL gets 40% weight in this calculation
        )
        
        return min(hybrid_score, 100)  # Cap at 100
    
    def train_model(self, training_data):
        """Train the ML component"""
        self.ml_model.train(training_data)

# Test function
def test_phishing_detector():
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
    ]
    
    detector = PhishingDetector()
    detector.train_model(training_data)
    
    # Test email content
    test_email = """From: fake-bank@example.com
To: victim@gmail.com
Subject: URGENT: Account Security Alert
Reply-To: security@fake-bank.com

Dear Customer,

Your account has been suspended. Please click here to verify:
http://fake-bank-login.com/verify

Click now to secure your account!
"""
    
    result = detector.analyze_email(test_email)
    
    print("=== Phishing Detector Test Results ===")
    print(f"Is Phishing: {result['is_phishing']}")
    print(f"Overall Confidence Score: {result['confidence_score']:.2f}")
    print(f"Rule Score: {result['rule_score']}")
    print(f"ML Prediction: {result['ml_prediction']} (Confidence: {result['ml_confidence']:.2f})")
    print(f"URL Score: {result['url_score']}")
    print(f"Rule Reasons: {result['rule_reasons']}")
    print(f"URL Reasons: {result['url_reasons']}")
    
    return result

if __name__ == "__main__":
    test_phishing_detector()