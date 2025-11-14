from config import Config

def test_config():
    print("=== Configuration Test Results ===")
    print(f"ML Weight: {Config.ML_WEIGHT}")
    print(f"Rule Weight: {Config.RULE_WEIGHT}")
    print(f"Phishing Threshold: {Config.PHISHING_THRESHOLD}")
    print(f"Model Path: {Config.MODEL_PATH}")
    print(f"Max Features: {Config.MAX_FEATURES}")
    print("Configuration loaded successfully!")

if __name__ == "__main__":
    test_config()