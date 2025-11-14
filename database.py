import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path='phishing_detector.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create analysis results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_content TEXT,
                is_phishing BOOLEAN,
                confidence_score REAL,
                rule_score REAL,
                ml_prediction INTEGER,
                ml_confidence REAL,
                url_score REAL,
                rule_reasons TEXT,
                url_reasons TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create known malicious URLs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS malicious_urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reported_by TEXT DEFAULT 'system'
            )
        ''')
        
        # Create known malicious domains table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS malicious_domains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reported_by TEXT DEFAULT 'system'
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    
    def save_analysis_result(self, email_content, result):
        """Save analysis result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analysis_results 
            (email_content, is_phishing, confidence_score, rule_score, 
             ml_prediction, ml_confidence, url_score, rule_reasons, url_reasons)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email_content,
            result.get('is_phishing', False),
            result.get('confidence_score', 0),
            result.get('rule_score', 0),
            result.get('ml_prediction', 0),
            result.get('ml_confidence', 0),
            result.get('url_score', 0),
            ', '.join(result.get('rule_reasons', [])),
            ', '.join(result.get('url_reasons', []))
        ))
        
        conn.commit()
        conn.close()
    
    def get_analysis_history(self, limit=10):
        """Get recent analysis results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analysis_results 
            ORDER BY analyzed_at DESC LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def add_malicious_url(self, url, reported_by='system'):
        """Add a URL to the malicious URLs list"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO malicious_urls (url, reported_by) VALUES (?, ?)
            ''', (url, reported_by))
            conn.commit()
            print(f"Added malicious URL: {url}")
        except sqlite3.IntegrityError:
            # URL already exists
            print(f"URL already in database: {url}")
        
        conn.close()
    
    def add_malicious_domain(self, domain, reported_by='system'):
        """Add a domain to the malicious domains list"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO malicious_domains (domain, reported_by) VALUES (?, ?)
            ''', (domain, reported_by))
            conn.commit()
            print(f"Added malicious domain: {domain}")
        except sqlite3.IntegrityError:
            # Domain already exists
            print(f"Domain already in database: {domain}")
        
        conn.close()
    
    def get_malicious_urls(self):
        """Get all known malicious URLs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT url FROM malicious_urls')
        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results]
    
    def get_malicious_domains(self):
        """Get all known malicious domains"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT domain FROM malicious_domains')
        results = cursor.fetchall()
        conn.close()
        return [row[0] for row in results]

# Test function
def test_database():
    db = Database()
    
    print("=== Database Test Results ===")
    
    # Test adding malicious URLs
    db.add_malicious_url("http://fake-bank.com/login", "test")
    db.add_malicious_url("http://suspicious-site.com", "test")
    
    # Test adding malicious domains
    db.add_malicious_domain("fake-bank.com", "test")
    db.add_malicious_domain("suspicious-site.com", "test")
    
    # Show malicious lists
    print(f"Malicious URLs: {db.get_malicious_urls()}")
    print(f"Malicious Domains: {db.get_malicious_domains()}")
    
    # Test saving an analysis result
    sample_result = {
        'is_phishing': True,
        'confidence_score': 85.5,
        'rule_score': 60,
        'ml_prediction': 1,
        'ml_confidence': 0.9,
        'url_score': 70,
        'rule_reasons': ['suspicious domain', 'urgent language'],
        'url_reasons': ['IP address in URL']
    }
    
    db.save_analysis_result("Sample email content", sample_result)
    
    # Get recent analysis results
    history = db.get_analysis_history(5)
    print(f"Analysis history count: {len(history)}")
    
    print("Database test completed successfully!")

if __name__ == "__main__":
    test_database()