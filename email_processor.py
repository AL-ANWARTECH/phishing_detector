import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from threading import Thread
import queue
from phishing_detector import PhishingDetector
from database import Database
from logger import get_logger
from config import Config

class EmailProcessor:
    def __init__(self):
        self.detector = PhishingDetector()
        self.db = Database()
        self.logger = get_logger()
        self.config = Config()
        self.processing_queue = queue.Queue()
        self.is_running = False
        self.processing_thread = None
    
    def add_email_to_queue(self, email_content):
        """Add email to processing queue"""
        self.processing_queue.put(email_content)
        self.logger.info(f"Email added to processing queue. Queue size: {self.processing_queue.qsize()}")
    
    def process_email_from_queue(self):
        """Process emails from the queue in a separate thread"""
        while self.is_running:
            try:
                if not self.processing_queue.empty():
                    email_content = self.processing_queue.get(timeout=1)
                    self.process_single_email(email_content)
                    self.processing_queue.task_done()
                else:
                    time.sleep(0.1)  # Small delay to prevent busy waiting
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error processing email from queue: {str(e)}")
    
    def process_single_email(self, email_content):
        """Process a single email"""
        try:
            self.logger.info("Processing email from queue")
            result = self.detector.analyze_email(email_content)
            
            # Save to database
            self.db.save_analysis_result(email_content, result)
            
            # Log the result
            status = "PHISHING" if result['is_phishing'] else "SAFE"
            self.logger.info(f"Email processed - Status: {status}, Score: {result['confidence_score']:.2f}%")
            
            return result
        except Exception as e:
            self.logger.error(f"Error processing single email: {str(e)}")
            return {'error': str(e)}
    
    def start_processing(self):
        """Start the email processing thread"""
        if not self.is_running:
            self.is_running = True
            self.processing_thread = Thread(target=self.process_email_from_queue, daemon=True)
            self.processing_thread.start()
            self.logger.info("Email processing started")
    
    def stop_processing(self):
        """Stop the email processing thread"""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
        self.logger.info("Email processing stopped")
    
    def process_imap_emails(self, server, username, password, folder='INBOX'):
        """Process emails from an IMAP server"""
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(server)
            mail.login(username, password)
            mail.select(folder)
            
            # Search for all emails
            status, messages = mail.search(None, 'ALL')
            email_ids = messages[0].split()
            
            processed_count = 0
            for email_id in email_ids[-10:]:  # Process last 10 emails to avoid too many
                # Fetch email
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                email_body = msg_data[0][1]
                
                # Parse email
                email_message = email.message_from_bytes(email_body)
                
                # Convert to string format for processing
                email_content = email_message.as_string()
                
                # Add to processing queue
                self.add_email_to_queue(email_content)
                processed_count += 1
            
            mail.close()
            mail.logout()
            self.logger.info(f"Processed {processed_count} emails from IMAP server")
            
            return processed_count
        except Exception as e:
            self.logger.error(f"Error processing IMAP emails: {str(e)}")
            return 0
    
    def send_email_alert(self, email_address, result, original_email_content):
        """Send an alert email if phishing is detected"""
        try:
            # This is a placeholder - in production, you'd configure SMTP settings
            subject = "Phishing Alert - Suspicious Email Detected"
            body = f"""
            A suspicious email has been detected by the phishing detection system.

            Detection Result:
            - Status: {'PHISHING DETECTED' if result['is_phishing'] else 'SAFE'}
            - Confidence Score: {result['confidence_score']:.2f}%
            - Rule Score: {result['rule_score']}%
            - ML Prediction: {result['ml_prediction']} (Confidence: {result['ml_confidence']:.2f})
            - URL Score: {result['url_score']}%

            Rule Reasons: {', '.join(result.get('rule_reasons', []))}
            URL Reasons: {', '.join(result.get('url_reasons', []))}

            Original email content has been logged for review.
            """
            
            self.logger.info(f"Phishing alert prepared for {email_address}")
            # In production, you would send the actual email here
            return True
        except Exception as e:
            self.logger.error(f"Error sending alert email: {str(e)}")
            return False
    
    def batch_process_emails(self, email_list):
        """Process multiple emails in batch"""
        results = []
        
        for email_content in email_list:
            result = self.process_single_email(email_content)
            results.append(result)
        
        self.logger.info(f"Batch processed {len(email_list)} emails")
        return results

# API wrapper for email processing
class EmailProcessingAPI:
    def __init__(self):
        self.processor = EmailProcessor()
        self.logger = get_logger()
    
    def start_processing_service(self):
        """Start the email processing service"""
        self.processor.start_processing()
        self.logger.info("Email processing service started")
    
    def stop_processing_service(self):
        """Stop the email processing service"""
        self.processor.stop_processing()
        self.logger.info("Email processing service stopped")
    
    def add_email_for_processing(self, email_content):
        """Add an email for processing"""
        self.processor.add_email_to_queue(email_content)
        return {"status": "added_to_queue", "queue_size": self.processor.processing_queue.qsize()}
    
    def get_processing_status(self):
        """Get current processing status"""
        return {
            "is_running": self.processor.is_running,
            "queue_size": self.processor.processing_queue.qsize(),
            "processed_count": "N/A"  # Would need to track this separately
        }

# Test function
def test_email_processor():
    print("=== Email Processor Test ===")
    
    processor = EmailProcessor()
    
    # Sample phishing email
    sample_email = """From: fake-bank@example.com
To: victim@gmail.com
Subject: URGENT: Account Security Alert
Reply-To: security@fake-bank.com

Dear Customer,

Your account has been suspended. Please click here to verify:
http://fake-bank-login.com/verify

Click now to secure your account!
"""
    
    # Add email to queue
    processor.add_email_to_queue(sample_email)
    print(f"Email added to queue. Queue size: {processor.processing_queue.qsize()}")
    
    # Start processing
    processor.start_processing()
    print("Processing started")
    
    # Wait a bit for processing
    time.sleep(2)
    
    # Stop processing
    processor.stop_processing()
    print("Processing stopped")
    
    print("Email processor test completed!")

if __name__ == "__main__":
    test_email_processor()