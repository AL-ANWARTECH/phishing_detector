# Phishing Detection System

A comprehensive phishing detection system that combines rule-based and machine learning approaches to identify phishing emails.

## Features

- **Email Parsing**: Extracts features from email content including subject, body, sender, links, and attachments
- **Rule-Based Detection**: Identifies suspicious patterns and domains using predefined rules
- **Machine Learning**: Uses a Naive Bayes classifier to detect phishing patterns
- **Hybrid Scoring**: Combines rule-based and ML scores for accurate detection
- **Web Interface**: User-friendly web interface built with Flask
- **API Access**: RESTful API for programmatic access

## Architecture

The system consists of four main components:

1. **Email Parser**: Extracts features from email content
2. **Rule Engine**: Applies predefined rules to detect suspicious patterns
3. **ML Model**: Uses machine learning to identify phishing indicators
4. **Phishing Detector**: Combines all components into a unified system

## Installation

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd phishing_detector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Interface

1. Start the application:

   ```bash
   python main.py
   ```

2. Open your browser and go to `http://localhost:5000`

3. Paste email content in the text area and click "Analyze Email"

### API Usage

Analyze an email via API:

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"email_content": "Your email content here"}'
```

Health check:

```bash
curl http://localhost:5000/health
```

## Configuration

The system uses a configuration file (`config.py`) with the following settings:

- `ML_WEIGHT`: Weight for machine learning component (default: 0.7)
- `RULE_WEIGHT`: Weight for rule-based component (default: 0.3)
- `PHISHING_THRESHOLD`: Score threshold for phishing detection (default: 50)

## API Endpoints

- `GET /` - Web interface
- `POST /analyze` - Analyze email content
- `GET /health` - Health check

## Response Format

```json
{
  "is_phishing": true,
  "confidence_score": 75.5,
  "rule_score": 60,
  "ml_prediction": 1,
  "ml_confidence": 0.9,
  "rule_reasons": ["Suspicious keyword in subject: urgent"],
  "features": { ... }
}
```

## Components

### Email Parser (`email_parser.py`)

- Parses email content
- Extracts subject, body, sender, links, and attachments
- Identifies sender and reply-to domains

### Rule Engine (`rule_engine.py`)

- Checks for suspicious domains
- Identifies domain mismatches
- Detects suspicious keywords and patterns
- Evaluates urgency indicators

### ML Model (`ml_model.py`)

- Uses Naive Bayes algorithm
- Analyzes text content for phishing indicators
- Provides prediction confidence

### Phishing Detector (`phishing_detector.py`)

- Integrates all components
- Calculates hybrid score
- Provides final phishing determination

## Training Data

The system can be trained with labeled email data in the format:

```python
[
  (email_features, label),  # label: 0 = legitimate, 1 = phishing
  ...
]
```

## Development

To extend the system:

1. Add more rules to the Rule Engine
2. Improve the ML model with more sophisticated algorithms
3. Add new features to the email parser
4. Enhance the web interface with additional functionality

## License

This project is open source and available under the MIT License.

````

## **Step 8 Git Commit:**

After creating the README file, run:

```bash
git add README.md
git commit -m "docs: add project documentation and usage instructions"
````

✅ **SUCCESS**: When you see the commit is successful, Step 8 is complete!

## **Project Completion!**

I have successfully built a complete phishing detection system with:

- ✅ Email parsing functionality
- ✅ Rule-based detection engine
- ✅ Machine learning model
- ✅ Configuration system
- ✅ Integrated phishing detector
- ✅ Web interface with Flask
- ✅ Dependencies management
- ✅ Complete documentation

Your system is now ready to use! You can run it with:

```bash
py main.py
```

And access it at `http://localhost:5000`
