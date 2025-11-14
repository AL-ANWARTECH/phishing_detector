````
# Phishing Detection System - User Manual

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Web Interface](#web-interface)
5. [API Usage](#api-usage)
6. [Command Line Interface](#command-line-interface)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)

## Overview

The Phishing Detection System is a comprehensive tool that combines rule-based and machine learning approaches to identify phishing emails. It provides multiple interfaces for different use cases.

### Features
- Real-time email analysis
- Web interface for manual analysis
- RESTful API for integration
- Command line interface for batch processing
- Database storage for analysis history
- Advanced URL analysis
- Logging and monitoring

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd phishing_detector
````

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python main.py
   ```

## Quick Start

### Web Interface

1. Start the application:

   ```bash
   python main.py
   ```

2. Open your browser and go to `http://localhost:5000`

3. Paste an email content in the text area and click "Analyze Email"

### Command Line Interface

```bash
# Analyze a single email file
python cli.py analyze --file email.txt

# Analyze with verbose output
python cli.py analyze --file email.txt --verbose

# Show analysis history
python cli.py history

# Train the model
python cli.py train
```

## Web Interface

### Main Analysis Page

- Paste email content in the text area
- Click "Analyze Email" button
- View detailed results including:
  - Overall confidence score
  - Rule-based score
  - ML prediction and confidence
  - URL analysis score
  - Specific reasons for detection

### History Page

- View recent analysis results
- See phishing detection statistics
- Track system performance over time

## API Usage

### Analyze Email

- **Endpoint**: `POST /analyze`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "email_content": "Email content to analyze..."
  }
  ```
- **Response**:
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

### Get History

- **Endpoint**: `GET /history`
- **Response**: Array of recent analysis results

### Health Check

- **Endpoint**: `GET /health`
- **Response**: System health status

### Get Statistics

- **Endpoint**: `GET /stats`
- **Response**: System usage statistics

## Command Line Interface

### Commands

#### analyze

Analyze a single email file or content.

Options:

- `--file, -f`: Path to email file
- `--text, -t`: Email content as text
- `--verbose, -v`: Show detailed output

Examples:

```bash
python cli.py analyze --file email.txt
python cli.py analyze --text "From: fake@bank.com..."
python cli.py analyze --file email.txt --verbose
```

#### history

Show analysis history.

Options:

- `--limit, -l`: Number of results to show (default: 10)

Example:

```bash
python cli.py history --limit 20
```

#### train

Train the machine learning model.

Options:

- `--file`: Path to training data file

Example:

```bash
python cli.py train
```

#### evaluate

Evaluate model performance.

Example:

```bash
python cli.py evaluate
```

#### process-dir

Process all email files in a directory.

Example:

```bash
python cli.py process-dir /path/to/emails
```

#### batch

Batch process emails from a JSON file.

Example:

```bash
python cli.py batch input.json --output results.json
```

## Configuration

### Configuration File Location

`config.py` contains all system configuration settings.

### Key Settings

- `PHISHING_THRESHOLD`: Score threshold for phishing detection (default: 50)
- `ML_WEIGHT`: Weight for machine learning component (default: 0.7)
- `RULE_WEIGHT`: Weight for rule-based component (default: 0.3)
- `URL_WEIGHT`: Weight for URL analysis component (default: 0.4)
- `LOG_LEVEL`: Logging level (default: 'INFO')

### Database Configuration

- `DB_PATH`: Path to SQLite database file
- `ENABLE_DATABASE_LOGGING`: Enable/disable database logging
- `ENABLE_HISTORY_TRACKING`: Enable/disable history tracking

## Troubleshooting

### Common Issues

#### Application won't start

- Check Python version (must be 3.8+)
- Verify all dependencies are installed
- Check port 5000 is not in use

#### Analysis results are not accurate

- Train the model with more data
- Adjust threshold values in config
- Add more suspicious patterns to rule engine

#### Database errors

- Check file permissions
- Verify database path exists
- Check for database corruption

#### API returns errors

- Verify JSON format in requests
- Check content type headers
- Review logs for specific error messages

### Logging

- Log files are stored in the `logs/` directory
- Files are named with date stamps
- Review logs for detailed error information

### Getting Help

- Check the logs directory for error details
- Verify all dependencies are installed
- Ensure all required files are present
- Contact system administrator for assistance

## Best Practices

### For Accuracy

- Regularly update training data
- Add new suspicious patterns to rules
- Monitor false positive rates
- Fine-tune threshold values

### For Performance

- Use appropriate hardware resources
- Monitor system resource usage
- Implement proper logging
- Regular backup of data

### For Security

- Use HTTPS in production
- Implement proper authentication
- Regular security updates
- Monitor for suspicious activity

```

```
