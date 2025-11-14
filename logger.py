import logging
from config import Config
from datetime import datetime
import os

class Logger:
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger('phishing_detector')
    
    def setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(Config.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(Config.LOG_FILE)
        file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
        console_handler.setFormatter(formatter)
        
        # Get logger and add handlers
        logger = logging.getLogger('phishing_detector')
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        self.logger = logger
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)

# Global logger instance
logger = Logger()

def get_logger():
    """Get the global logger instance"""
    return logger

# Test function
def test_logger():
    logger = get_logger()
    logger.info("Logger test: System started")
    logger.warning("Logger test: Suspicious activity detected")
    logger.error("Logger test: Error occurred")
    print("Logger test completed. Check the logs folder for log files.")

if __name__ == "__main__":
    test_logger()