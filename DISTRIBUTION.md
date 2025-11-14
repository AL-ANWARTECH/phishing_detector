````markdown
# Phishing Detection System - Distribution Package

## Overview

This package contains the complete Phishing Detection System with all necessary components for deployment.

## Package Contents

### Core Components

- `phishing_detector/` - Main application source code
- `main.py` - Web interface and API server
- `cli.py` - Command line interface
- `analytics_dashboard.py` - Performance monitoring dashboard

### Configuration Files

- `config.py` - System configuration
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Container orchestration

### Documentation

- `README.md` - Main documentation
- `USER_MANUAL.md` - User guide
- `API_DOCS.md` - API documentation
- `INSTALLATION.md` - Installation guide
- `DEPLOYMENT.md` - Deployment guide

## Installation Methods

### Method 1: Using Installation Scripts (Recommended)

#### On Linux/macOS:

```bash
chmod +x install.sh
./install.sh
```
````

#### On Windows:

```cmd
install.bat
```

### Method 2: Manual Installation

1. Create virtual environment:

```bash
python -m venv phishing_env
source phishing_env/bin/activate  # Linux/macOS
# or
phishing_env\Scripts\activate  # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize database:

```bash
python -c "from database import Database; Database()"
```

### Method 3: Using pip (for development)

```bash
pip install -e .
```

## Running the Application

### Web Interface

```bash
python main.py
```

Access at: http://localhost:5000

### Command Line Interface

```bash
python cli.py analyze --file email.txt
```

### Analytics Dashboard

```bash
python analytics_dashboard.py
```

Access at: http://localhost:5001/analytics

## Production Deployment

### Using Docker

```bash
docker-compose up --build -d
```

### Using Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class gevent --worker-connections 1000 wsgi:app
```

## Package Structure

```
phishing_detector/
├── main.py                 # Main web application
├── cli.py                  # Command line interface
├── phishing_detector.py    # Core detection logic
├── email_parser.py         # Email parsing
├── rule_engine.py          # Rule-based detection
├── ml_model.py             # Machine learning model
├── url_analyzer.py         # URL analysis
├── database.py             # Database operations
├── config.py               # Configuration
├── logger.py               # Logging system
├── performance_monitor.py  # Performance monitoring
├── analytics_dashboard.py  # Analytics dashboard
├── test_phishing_detector.py # Unit tests
├── integration_tests.py    # Integration tests
├── run_tests.py           # Test runner
├── setup.py               # Package setup
├── install.sh             # Linux/Mac installation
├── install.bat            # Windows installation
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker orchestration
├── requirements.txt       # Dependencies
├── requirements-packaging.txt # Packaging dependencies
├── build_package.py       # Package builder
├── README.md              # Main documentation
├── USER_MANUAL.md         # User guide
├── API_DOCS.md            # API documentation
├── INSTALLATION.md        # Installation guide
├── DEPLOYMENT.md          # Deployment guide
├── DISTRIBUTION.md        # Distribution guide
├── logs/                  # Log files
├── models/                # ML models
└── data/                  # Data files
```

## System Requirements

### Minimum Requirements

- Python 3.8+
- 2GB RAM
- 500MB disk space
- Modern CPU with 2+ cores

### Recommended Requirements

- Python 3.9+
- 4GB+ RAM
- 1GB+ disk space
- Multi-core processor

## Support

For support, please:

1. Check the logs directory for error details
2. Review the documentation files
3. Contact the system administrator
4. Create an issue in the repository
