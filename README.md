# Updated README.md

Here's your updated README.md with all the new features and improvements:

````markdown
# Phishing Detection System

A comprehensive phishing detection system that combines rule-based and machine learning approaches to identify phishing emails in real-time.

## 🚀 Features

- **Multi-layered Detection**: Combines rule-based, ML, and URL analysis
- **Real-time Analysis**: Instant phishing detection
- **Multiple Interfaces**: Web UI, CLI, and REST API
- **Performance Monitoring**: Real-time system metrics
- **Historical Tracking**: Analysis history and statistics
- **Advanced ML**: Naive Bayes and Random Forest algorithms
- **URL Analysis**: Suspicious link detection
- **Database Storage**: SQLite for results and history
- **Comprehensive Logging**: Detailed system logging
- **Production Ready**: Docker deployment support

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Command Line Interface](#command-line-interface)
- [Web Interface](#web-interface)
- [Performance Monitoring](#performance-monitoring)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Installation

#### Using Installation Scripts (Recommended)

**Linux/macOS:**

```bash
chmod +x install.sh
./install.sh
```
````

**Windows:**

```cmd
install.bat
```

#### Manual Installation

```bash
# Clone the repository
git clone <repository-url>
cd phishing_detector

# Create virtual environment
python -m venv phishing_env
source phishing_env/bin/activate  # Linux/macOS
# or
phishing_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from database import Database; Database()"
```

## 🚀 Quick Start

### Start Web Interface

```bash
python main.py
```

Visit `http://localhost:5000`

### Command Line Analysis

```bash
python cli.py analyze --file email.txt --verbose
```

### Performance Dashboard

```bash
python analytics_dashboard.py
```

Visit `http://localhost:5001/analytics`

## 📖 Usage

### Web Interface

1. Navigate to `http://localhost:5000`
2. Paste email content in the text area
3. Click "Analyze Email"
4. View detailed results including confidence scores and reasons

### Command Line Interface

```bash
# Analyze single email file
python cli.py analyze --file email.txt

# Analyze with verbose output
python cli.py analyze --file email.txt --verbose

# Show analysis history
python cli.py history

# Train the model
python cli.py train

# Process directory of emails
python cli.py process-dir /path/to/emails
```

### API Usage

```bash
# Analyze email via API
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"email_content": "From: fake-bank@example.com\nSubject: URGENT: Verify Account\n\nClick here: http://fake.com"}'
```

## 🌐 API Documentation

### Endpoints

- `POST /analyze` - Analyze email content
- `GET /history` - Get analysis history
- `GET /health` - Health check
- `GET /stats` - System statistics
- `GET /analytics` - Performance dashboard

### Response Format

```json
{
  "is_phishing": true,
  "confidence_score": 75.5,
  "rule_score": 60,
  "ml_prediction": 1,
  "ml_confidence": 0.9,
  "url_score": 70,
  "rule_reasons": ["suspicious domain", "urgent language"],
  "url_reasons": ["IP address in URL"]
}
```

## 📊 Performance Monitoring

The system includes comprehensive performance monitoring:

- **Real-time Metrics**: CPU, memory, disk usage
- **Analysis Statistics**: Times, success rates, phishing rates
- **Historical Data**: Trend analysis
- **Visual Dashboard**: Interactive charts

Access the dashboard at `http://localhost:5001/analytics`

## ⚙️ Configuration

System configuration is managed in `config.py`:

```python
class Config:
    # Feature weights
    ML_WEIGHT = 0.7
    RULE_WEIGHT = 0.3
    URL_WEIGHT = 0.4

    # Thresholds
    PHISHING_THRESHOLD = 50

    # Database
    DB_PATH = 'phishing_detector.db'

    # Logging
    LOG_LEVEL = 'INFO'
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python run_tests.py
```

Or run specific tests:

```bash
python run_tests.py unit      # Unit tests
python run_tests.py integration  # Integration tests
```

## 🚢 Deployment

### Development

```bash
python main.py
```

### Production with Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class gevent wsgi:app
```

### Docker Deployment

```bash
docker-compose up --build -d
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   CLI           │    │   API Client    │
│   (Flask)       │    │   (Python)      │    │   (REST)        │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │    Phishing Detector      │
                    │    (Main Logic)           │
                    └─────────────┬─────────────┘
                                 │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
┌───────▼────────┐    ┌──────────▼────────┐    ┌──────────▼────────┐
│   Rule Engine  │    │   ML Model        │    │   URL Analyzer    │
│   (Rules)      │    │   (Patterns)      │    │   (Links)         │
└────────────────┘    └───────────────────┘    └───────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │      Database             │
                    │      (SQLite)             │
                    └───────────────────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support:

- Check the documentation files
- Review the logs directory
- Create an issue in the repository
- Contact the development team

## 🙏 Acknowledgments

- The Python community for excellent libraries
- Open source contributors who made this possible
- Security researchers for phishing detection insights
- Users who help improve the system

---

**Made with ❤️ for a safer internet**

_Report issues, suggest features, or contribute to make this system even better!_

```

```
