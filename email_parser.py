import email
import re
from urllib.parse import urlparse

class EmailParser:
    def __init__(self):
        pass
    
    def parse_email(self, email_content):
        """Parse email content and extract features"""
        msg = email.message_from_string(email_content)
        
        features = {
            'subject': msg.get('Subject', ''),
            'from_address': msg.get('From', ''),
            'to_address': msg.get('To', ''),
            'reply_to': msg.get('Reply-To', ''),
            'body': self.extract_body(msg),
            'links': self.extract_links(msg),
            'attachments': self.count_attachments(msg),
            'sender_domain': self.extract_sender_domain(msg.get('From', '')),
            'reply_domain': self.extract_reply_domain(msg.get('Reply-To', ''))
        }
        
        return features
    
    def extract_body(self, msg):
        """Extract email body content"""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                elif part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        return body
    
    def extract_links(self, msg):
        """Extract all links from email"""
        body = self.extract_body(msg)
        # Find URLs in the body
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        links = re.findall(url_pattern, body)
        return links
    
    def count_attachments(self, msg):
        """Count email attachments"""
        count = 0
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_disposition() == 'attachment':
                    count += 1
        return count
    
    def extract_sender_domain(self, from_header):
        """Extract domain from sender email"""
        if '<' in from_header:
            domain = from_header.split('@')[-1].split('>')[0]
        else:
            domain = from_header.split('@')[-1] if '@' in from_header else ''
        return domain.strip()
    
    def extract_reply_domain(self, reply_to):
        """Extract domain from reply-to header"""
        if reply_to and '@' in reply_to:
            domain = reply_to.split('@')[-1]
            return domain.strip()
        return ''

# Test function
def test_email_parser():
    # Sample email content for testing
    sample_email = """From: fake-bank@example.com
To: victim@gmail.com
Subject: URGENT: Account Security Alert
Reply-To: security@fake-bank.com

Dear Customer,

Your account has been suspended. Please click here to verify:
http://fake-bank-login.com/verify

Click now to secure your account!
"""
    
    parser = EmailParser()
    features = parser.parse_email(sample_email)
    
    print("=== Email Parser Test Results ===")
    for key, value in features.items():
        print(f"{key}: {value}")
    
    return features

if __name__ == "__main__":
    test_email_parser()