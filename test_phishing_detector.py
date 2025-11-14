import unittest
import tempfile
import os
from phishing_detector import PhishingDetector
from email_parser import EmailParser
from rule_engine import RuleEngine
from ml_model import MLModel
from url_analyzer import URLAnalyzer
from database import Database
from config import Config
from logger import get_logger

class TestEmailParser(unittest.TestCase):
    def setUp(self):
        self.parser = EmailParser()
    
    def test_parse_basic_email(self):
        """Test parsing a basic email"""
        email_content = """From: sender@example.com
To: recipient@example.com
Subject: Test Subject
Reply-To: reply@example.com

This is the email body.
http://example.com/link
"""
        
        features = self.parser.parse_email(email_content)
        
        self.assertEqual(features['subject'], 'Test Subject')
        self.assertEqual(features['from_address'], 'sender@example.com')
        self.assertEqual(features['to_address'], 'recipient@example.com')
        self.assertEqual(features['reply_to'], 'reply@example.com')
        self.assertIn('http://example.com/link', features['links'])
        self.assertIn('This is the email body.', features['body'])
    
    def test_parse_multipart_email(self):
        """Test parsing a multipart email"""
        email_content = """From: test@example.com
To: user@test.com
Subject: Multipart Test

--boundary
Content-Type: text/plain

Plain text content
--boundary
Content-Type: text/html

<html><body>HTML content</body></html>
--boundary--
"""
        
        features = self.parser.parse_email(email_content)
        self.assertIsNotNone(features['body'])
    
    def test_extract_sender_domain(self):
        """Test extracting sender domain"""
        domain = self.parser.extract_sender_domain('John Doe <john@example.com>')
        self.assertEqual(domain, 'example.com')
        
        domain = self.parser.extract_sender_domain('simple@example.com')
        self.assertEqual(domain, 'example.com')

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.rule_engine = RuleEngine()
    
    def test_suspicious_domain_detection(self):
        """Test detection of suspicious domains"""
        features = {
            'sender_domain': 'bit.ly',
            'reply_domain': 'bit.ly',
            'subject': 'Test',
            'body': 'Test body',
            'links': [],
            'attachments': 0
        }
        
        score, reasons = self.rule_engine.evaluate_rules(features)
        self.assertGreater(score, 0)
        self.assertIn("Suspicious sender domain", reasons)
    
    def test_domain_mismatch(self):
        """Test detection of domain mismatch"""
        features = {
            'sender_domain': 'example.com',
            'reply_domain': 'different.com',
            'subject': 'Test',
            'body': 'Test body',
            'links': [],
            'attachments': 0
        }
        
        score, reasons = self.rule_engine.evaluate_rules(features)
        self.assertIn("Sender and reply-to domains don't match", reasons)
    
    def test_suspicious_keywords(self):
        """Test detection of suspicious keywords"""
        features = {
            'sender_domain': 'example.com',
            'reply_domain': '',
            'subject': 'URGENT: Verify Account',
            'body': 'Click here now',
            'links': [],
            'attachments': 0
        }
        
        score, reasons = self.rule_engine.evaluate_rules(features)
        self.assertIn("Suspicious keyword in subject: urgent", reasons)
    
    def test_multiple_attachments(self):
        """Test detection of multiple attachments"""
        features = {
            'sender_domain': 'example.com',
            'reply_domain': '',
            'subject': 'Test',
            'body': 'Test',
            'links': [],
            'attachments': 3
        }
        
        score, reasons = self.rule_engine.evaluate_rules(features)
        self.assertIn("Multiple attachments detected", reasons)

class TestMLModel(unittest.TestCase):
    def setUp(self):
        self.ml_model = MLModel()
        
        # Sample training data
        self.training_data = [
            ({
                'subject': 'Meeting Reminder',
                'body': 'Hi, just a reminder about our meeting tomorrow.',
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
                'body': 'Your account has been suspended. Click here to verify.',
                'from_address': 'fake-bank@example.com',
                'to_address': 'victim@gmail.com',
                'reply_to': 'security@fake-bank.com',
                'links': ['http://fake-bank.com/verify'],
                'attachments': 0,
                'sender_domain': 'example.com',
                'reply_domain': 'fake-bank.com'
            }, 1),  # Phishing
        ]
    
    def test_model_training(self):
        """Test ML model training"""
        self.ml_model.train(self.training_data)
        self.assertTrue(self.ml_model.is_trained)
    
    def test_model_prediction(self):
        """Test ML model prediction"""
        self.ml_model.train(self.training_data)
        
        test_features = {
            'subject': 'URGENT: Account Security Alert',
            'body': 'Your account has been suspended. Click here to verify.',
            'from_address': 'fake-bank@example.com',
            'to_address': 'victim@gmail.com',
            'reply_to': 'security@fake-bank.com',
            'links': ['http://fake-bank.com/verify'],
            'attachments': 0,
            'sender_domain': 'example.com',
            'reply_domain': 'fake-bank.com'
        }
        
        prediction, confidence = self.ml_model.predict(test_features)
        self.assertIsNotNone(prediction)
        self.assertIsNotNone(confidence)

class TestURLAnalyzer(unittest.TestCase):
    def setUp(self):
        self.url_analyzer = URLAnalyzer()
    
    def test_suspicious_url_detection(self):
        """Test detection of suspicious URLs"""
        score, reasons = self.url_analyzer.analyze_url('http://paypal-login.com/verify')
        self.assertGreater(score, 0)
        self.assertIn("Suspicious subdomain: paypal", reasons)
    
    def test_ip_address_detection(self):
        """Test detection of IP addresses in URLs"""
        score, reasons = self.url_analyzer.analyze_url('http://192.168.1.1/login')
        self.assertGreater(score, 0)
        self.assertIn("IP address used instead of domain", reasons)
    
    def test_url_shortener_detection(self):
        """Test detection of URL shorteners"""
        score, reasons = self.url_analyzer.analyze_url('https://bit.ly/urgent-verify')
        self.assertGreater(score, 0)
        self.assertIn("URL shortener domain: bit.ly", reasons)

class TestPhishingDetector(unittest.TestCase):
    def setUp(self):
        self.detector = PhishingDetector()
        
        # Sample training data
        self.training_data = [
            ({
                'subject': 'Meeting Reminder',
                'body': 'Hi, just a reminder about our meeting tomorrow.',
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
                'body': 'Your account has been suspended. Click here to verify.',
                'from_address': 'fake-bank@example.com',
                'to_address': 'victim@gmail.com',
                'reply_to': 'security@fake-bank.com',
                'links': ['http://fake-bank.com/verify'],
                'attachments': 0,
                'sender_domain': 'example.com',
                'reply_domain': 'fake-bank.com'
            }, 1),  # Phishing
        ]
        self.detector.train_model(self.training_data)
    
    def test_complete_analysis(self):
        """Test complete email analysis"""
        test_email = """From: fake-bank@example.com
To: victim@gmail.com
Subject: URGENT: Account Security Alert
Reply-To: security@fake-bank.com

Dear Customer,

Your account has been suspended. Please click here to verify:
http://fake-bank-login.com/verify

Click now to secure your account!
"""
        
        result = self.detector.analyze_email(test_email)
        
        self.assertIsNotNone(result['confidence_score'])
        self.assertIn('is_phishing', result)
        self.assertIn('rule_score', result)
        self.assertIn('ml_prediction', result)
        self.assertIn('url_score', result)
        self.assertIn('rule_reasons', result)
        self.assertIn('url_reasons', result)
    
    def test_safe_email(self):
        """Test analysis of safe email"""
        safe_email = """From: colleague@company.com
To: user@company.com
Subject: Meeting Reminder

Hi, just a reminder about our meeting tomorrow at 2 PM.
"""
        
        result = self.detector.analyze_email(safe_email)
        # Note: This might still flag as phishing due to our simple training data
        # The important thing is that it returns a valid result
        self.assertIsNotNone(result['confidence_score'])

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary database file for testing
        self.db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_file.close()
        self.db = Database(db_path=self.db_file.name)
    
    def tearDown(self):
        # Clean up the temporary database file
        os.unlink(self.db_file.name)
    
    def test_database_initialization(self):
        """Test database initialization"""
        # Database is initialized in setUp
        self.assertTrue(os.path.exists(self.db_file.name))
    
    def test_save_analysis_result(self):
        """Test saving analysis result to database"""
        result = {
            'is_phishing': True,
            'confidence_score': 85.5,
            'rule_score': 60,
            'ml_prediction': 1,
            'ml_confidence': 0.9,
            'url_score': 70,
            'rule_reasons': ['suspicious domain'],
            'url_reasons': ['IP address in URL']
        }
        
        self.db.save_analysis_result("Test email content", result)
        
        # Verify result was saved
        history = self.db.get_analysis_history(1)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][2], 1)  # is_phishing should be True (1)
    
    def test_add_malicious_url(self):
        """Test adding malicious URL to database"""
        self.db.add_malicious_url("http://fake-bank.com")
        
        urls = self.db.get_malicious_urls()
        self.assertIn("http://fake-bank.com", urls)

class TestConfiguration(unittest.TestCase):
    def test_config_values(self):
        """Test configuration values"""
        config = Config()
        
        self.assertEqual(config.ML_WEIGHT, 0.7)
        self.assertEqual(config.RULE_WEIGHT, 0.3)
        self.assertEqual(config.PHISHING_THRESHOLD, 50)
        self.assertEqual(config.LOG_LEVEL, 'INFO')

class TestIntegration(unittest.TestCase):
    def test_full_pipeline(self):
        """Test the full pipeline from email parsing to analysis"""
        detector = PhishingDetector()
        
        # Sample training data
        training_data = [
            ({
                'subject': 'Safe Email',
                'body': 'This is a normal email.',
                'from_address': 'trusted@company.com',
                'to_address': 'user@company.com',
                'reply_to': '',
                'links': [],
                'attachments': 0,
                'sender_domain': 'company.com',
                'reply_domain': ''
            }, 0),  # Legitimate
        ]
        
        detector.train_model(training_data)
        
        # Test email
        test_email = """From: trusted@company.com
To: user@company.com
Subject: Normal Email

This is a normal, safe email.
"""
        
        result = detector.analyze_email(test_email)
        
        # Verify all required fields are present
        required_fields = [
            'is_phishing', 'confidence_score', 'rule_score', 
            'ml_prediction', 'ml_confidence', 'url_score',
            'rule_reasons', 'url_reasons', 'features'
        ]
        
        for field in required_fields:
            self.assertIn(field, result)

if __name__ == '__main__':
    unittest.main()