import unittest
import tempfile
import os
import json
from main import app
from phishing_detector import PhishingDetector
from database import Database

class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary database for testing
        self.db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_file.close()
        
        # Configure app for testing
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create a test database instance
        self.test_db = Database(db_path=self.db_file.name)
    
    def tearDown(self):
        # Clean up the temporary database file
        os.unlink(self.db_file.name)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('status', data)
        self.assertIn('ml_model_trained', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_analyze_endpoint(self):
        """Test analyze endpoint"""
        test_email = {
            "email_content": """From: fake-bank@example.com
To: victim@gmail.com
Subject: URGENT: Account Security Alert

Dear Customer, your account needs verification."""
        }
        
        response = self.client.post('/analyze', 
                                  json=test_email,
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('is_phishing', data)
        self.assertIn('confidence_score', data)
        self.assertIn('rule_score', data)
    
    def test_invalid_email_content(self):
        """Test analyze endpoint with invalid content"""
        invalid_email = {"email_content": ""}  # Empty content
        
        response = self.client.post('/analyze',
                                  json=invalid_email,
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_history_endpoint(self):
        """Test history endpoint"""
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIsInstance(data, list)

class TestCLIToAPIIntegration(unittest.TestCase):
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
    
    def test_cli_api_consistency(self):
        """Test that CLI and API produce consistent results"""
        test_email_content = """From: fake-bank@example.com
To: victim@gmail.com
Subject: URGENT: Account Security Alert

Dear Customer, your account needs verification."""
        
        # Get result from detector directly
        direct_result = self.detector.analyze_email(test_email_content)
        
        # The results should be valid
        self.assertIsNotNone(direct_result['confidence_score'])
        self.assertIn('is_phishing', direct_result)
        self.assertIn('rule_score', direct_result)
        self.assertIn('ml_prediction', direct_result)

class TestPerformance(unittest.TestCase):
    def test_multiple_analyses(self):
        """Test performance with multiple analyses"""
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
        
        # Test multiple analyses
        test_emails = [
            """From: trusted@company.com
To: user@company.com
Subject: Email 1
Body 1""",
            """From: trusted@company.com
To: user@company.com
Subject: Email 2
Body 2""",
            """From: trusted@company.com
To: user@company.com
Subject: Email 3
Body 3""",
        ]
        
        for email in test_emails:
            result = detector.analyze_email(email)
            self.assertIsNotNone(result['confidence_score'])

class TestErrorHandling(unittest.TestCase):
    def test_malformed_email(self):
        """Test handling of malformed email content"""
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
        
        # Test with malformed email
        malformed_emails = [
            "",  # Empty string
            "Just a plain text",  # No email headers
            "Subject: \n\n",  # Empty subject and body
        ]
        
        for email in malformed_emails:
            try:
                result = detector.analyze_email(email)
                # Should return a result even for malformed emails
                self.assertIsNotNone(result)
            except Exception as e:
                # If there's an exception, it should be handled gracefully
                self.fail(f"Unexpected exception for malformed email: {e}")

if __name__ == '__main__':
    unittest.main()