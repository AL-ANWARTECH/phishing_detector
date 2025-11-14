import re

class RuleEngine:
    def __init__(self):
        # Known suspicious domains and patterns
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 't.co', 'ow.ly', 'bit.do',
            'tiny.cc', 'rebrand.ly', 'is.gd', 'v.gd'
        ]
        
        self.suspicious_keywords = [
            'urgent', 'immediate action', 'verify account', 'security alert',
            'login now', 'click here', 'limited time', 'act now',
            'bank', 'paypal', 'amazon', 'apple', 'microsoft'
        ]
        
        self.suspicious_patterns = [
            r'password.*reset',
            r'account.*suspended',
            r'confirm.*information',
            r'urgent.*action',
            r'click.*here.*now'
        ]
    
    def evaluate_rules(self, email_features):
        """Evaluate email against rule-based criteria"""
        score = 0
        reasons = []
        
        # Check 1: Suspicious sender domain
        sender_domain = email_features.get('sender_domain', '').lower()
        if sender_domain in self.suspicious_domains:
            score += 20
            reasons.append("Suspicious sender domain")
        
        # Check 2: Domain mismatch between sender and reply-to
        reply_domain = email_features.get('reply_domain', '').lower()
        if sender_domain and reply_domain and sender_domain != reply_domain:
            score += 15
            reasons.append("Sender and reply-to domains don't match")
        
        # Check 3: Suspicious subject keywords
        subject = email_features.get('subject', '').lower()
        for keyword in self.suspicious_keywords:
            if keyword in subject:
                score += 10
                reasons.append(f"Suspicious keyword in subject: {keyword}")
        
        # Check 4: Suspicious body patterns
        body = email_features.get('body', '').lower()
        for pattern in self.suspicious_patterns:
            if re.search(pattern, body, re.IGNORECASE):
                score += 10
                reasons.append(f"Suspicious pattern found in body")
        
        # Check 5: Too many links
        links = email_features.get('links', [])
        if len(links) > 5:
            score += 15
            reasons.append("Excessive number of links")
        
        # Check 6: Suspicious TLD (Top Level Domain) - simplified version
        suspicious_tlds = ['tk', 'ml', 'ga', 'cf', 'xyz']
        for tld in suspicious_tlds:
            if sender_domain.endswith(tld):
                score += 10
                reasons.append("Suspicious top-level domain")
        
        # Check 7: Urgency indicators
        urgency_indicators = ['urgent', 'immediate', 'asap', 'today', 'now']
        for indicator in urgency_indicators:
            if indicator in subject.lower() or indicator in body.lower():
                score += 5
                reasons.append("Urgency indicator detected")
        
        # Check 8: Suspicious attachment count
        attachments = email_features.get('attachments', 0)
        if attachments > 1:
            score += 10
            reasons.append("Multiple attachments detected")
        
        return min(score, 100), reasons

# Test function
def test_rule_engine():
    # Sample features from email parser
    sample_features = {
        'subject': 'URGENT: Account Security Alert',
        'from_address': 'fake-bank@example.com',
        'to_address': 'victim@gmail.com',
        'reply_to': 'security@fake-bank.com',
        'body': 'Dear Customer, Your account has been suspended. Please click here to verify: http://fake-bank-login.com/verify',
        'links': ['http://fake-bank-login.com/verify'],
        'attachments': 0,
        'sender_domain': 'example.com',
        'reply_domain': 'fake-bank.com'
    }
    
    rule_engine = RuleEngine()
    score, reasons = rule_engine.evaluate_rules(sample_features)
    
    print("=== Rule Engine Test Results ===")
    print(f"Rule Score: {score}")
    print(f"Reasons: {reasons}")
    
    return score, reasons

if __name__ == "__main__":
    test_rule_engine()