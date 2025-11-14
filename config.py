import os
from datetime import datetime

class Config:
    # Feature weights for hybrid scoring
    ML_WEIGHT = 0.7
    RULE_WEIGHT = 0.3
    URL_WEIGHT = 0.4  # New: URL analysis weight
    
    # Threshold settings
    PHISHING_THRESHOLD = 50  # Score above this is considered phishing
    URL_SUSPICIOUS_THRESHOLD = 20  # URL score above this is suspicious
    
    # Model settings
    MODEL_PATH = 'models/phishing_model.pkl'
    VECTORIZER_PATH = 'models/vectorizer.pkl'
    
    # Feature extraction settings
    MAX_FEATURES = 5000
    STOP_WORDS = 'english'
    
    # Logging settings
    LOG_LEVEL = 'INFO'
    LOG_FILE = f'logs/phishing_detector_{datetime.now().strftime("%Y%m%d")}.log'
    
    # Database settings
    DB_PATH = 'phishing_detector.db'
    
    # URL analysis settings
    MAX_URL_LENGTH = 100
    SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.work']
    URL_SHORTENERS = ['bit.ly', 'tinyurl.com', 't.co', 'ow.ly', 'bit.do', 'tiny.cc', 'rebrand.ly', 'is.gd', 'v.gd', 'goo.gl']
    
    # Email analysis settings
    MAX_SUBJECT_LENGTH = 100
    MAX_LINKS_PER_EMAIL = 10
    
    # Advanced features
    ENABLE_URL_ANALYSIS = True
    ENABLE_DATABASE_LOGGING = True
    ENABLE_HISTORY_TRACKING = True
    
    @classmethod
    def get_db_path(cls):
        """Get database path, creating directory if needed"""
        db_dir = os.path.dirname(cls.DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        return cls.DB_PATH
    
    @classmethod
    def get_log_path(cls):
        """Get log path, creating directory if needed"""
        log_dir = os.path.dirname(cls.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return cls.LOG_FILE

# Create directories if they don't exist
os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(Config.MODEL_PATH), exist_ok=True)