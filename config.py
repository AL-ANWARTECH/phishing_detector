class Config:
    # Feature weights for hybrid scoring
    ML_WEIGHT = 0.7
    RULE_WEIGHT = 0.3
    
    # Threshold settings
    PHISHING_THRESHOLD = 50  # Score above this is considered phishing
    
    # Model settings
    MODEL_PATH = 'models/phishing_model.pkl'
    VECTORIZER_PATH = 'models/vectorizer.pkl'
    
    # Feature extraction settings
    MAX_FEATURES = 5000
    STOP_WORDS = 'english'
    
    # Logging settings
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'phishing_detector.log'