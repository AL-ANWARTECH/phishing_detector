import re
from urllib.parse import urlparse
import socket

class URLAnalyzer:
    def __init__(self):
        # Known malicious domains database (simplified)
        self.malicious_domains = set([
            'bit.ly', 'tinyurl.com', 't.co', 'ow.ly', 'bit.do',
            'tiny.cc', 'rebrand.ly', 'is.gd', 'v.gd', 'goo.gl'
        ])
    
    def analyze_url(self, url):
        """Analyze a single URL for phishing indicators"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            score = 0
            reasons = []
            
            # Check if domain is in malicious list
            if domain in self.malicious_domains:
                score += 30
                reasons.append(f"URL shortener domain: {domain}")
            
            # Check for IP address instead of domain
            if self.is_ip_address(domain):
                score += 25
                reasons.append("IP address used instead of domain")
            
            # Check for suspicious TLDs
            if domain.endswith(('.tk', '.ml', '.ga', '.cf', '.xyz')):
                score += 20
                reasons.append(f"Suspicious TLD in: {domain}")
            
            # Check for subdomain that looks like a domain
            parts = domain.split('.')
            if len(parts) >= 3:
                # Check if middle part looks like a well-known domain
                for part in parts[1:-1]:
                    if part in ['paypal', 'amazon', 'microsoft', 'google', 'apple', 'bank']:
                        score += 35
                        reasons.append(f"Suspicious subdomain: {part}")
            
            # Check URL length (very long URLs can be suspicious)
            if len(url) > 100:
                score += 10
                reasons.append("Very long URL")
            
            # Check for suspicious characters
            if '@' in url[8:]:  # After protocol
                score += 25
                reasons.append("Suspicious @ character in URL")
            
            return min(score, 100), reasons
            
        except Exception as e:
            return 0, [f"Error analyzing URL: {str(e)}"]
    
    def is_ip_address(self, domain):
        """Check if domain is actually an IP address"""
        try:
            socket.inet_aton(domain)
            return True
        except socket.error:
            return False
    
    def analyze_email_urls(self, email_features):
        """Analyze all URLs in an email"""
        links = email_features.get('links', [])
        total_score = 0
        all_reasons = []
        
        for url in links:
            url_score, reasons = self.analyze_url(url)
            total_score += url_score
            all_reasons.extend(reasons)
        
        # Normalize score based on number of URLs
        if links:
            avg_score = total_score / len(links)
        else:
            avg_score = 0
        
        return min(avg_score, 100), all_reasons

# Test function
def test_url_analyzer():
    analyzer = URLAnalyzer()
    
    test_urls = [
        'http://paypal-login.com/verify',
        'https://bit.ly/urgent-verify',
        'http://192.168.1.1/login',
        'https://secure-bank.com/account'
    ]
    
    print("=== URL Analysis Test Results ===")
    for url in test_urls:
        score, reasons = analyzer.analyze_url(url)
        print(f"URL: {url}")
        print(f"  Score: {score}")
        print(f"  Reasons: {reasons}")
        print()

if __name__ == "__main__":
    test_url_analyzer()