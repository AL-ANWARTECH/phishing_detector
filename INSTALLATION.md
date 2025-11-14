````
# Phishing Detection System - Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 7+, macOS 10.12+, Linux (any recent distribution)
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB available space
- **Processor**: Any modern CPU with 2+ cores

### Recommended Requirements
- **RAM**: 4GB or more
- **Disk Space**: 1GB available space
- **Processor**: Multi-core processor
- **Network**: Internet connection for updates

## Prerequisites

### Python Installation
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   # or
   python3 --version
````

### Git Installation (Optional)

- Download from [git-scm.com](https://git-scm.com/downloads)
- Or clone repository manually

## Installation Methods

### Method 1: Clone from Repository (Recommended)

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd phishing_detector
   ```

2. **Create virtual environment (recommended):**

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Method 2: Manual Installation

1. **Download the source code:**

   - Download ZIP file from repository
   - Extract to desired location

2. **Navigate to directory:**

   ```bash
   cd path/to/phishing_detector
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

### Required Dependencies

- Flask==2.3.2
- requests==2.31.0
- beautifulsoup4==4.12.2
- scikit-learn==1.3.0
- gunicorn==21.2.0 (production)
- gevent==23.9.1 (production)

### Optional Dependencies

- Docker (for containerization)
- Docker Compose (for orchestration)

## Virtual Environment Setup (Recommended)

Using a virtual environment prevents conflicts with other Python projects:

```bash
# Create virtual environment
python -m venv phishing_env

# Activate virtual environment
# On Windows:
phishing_env\Scripts\activate
# On macOS/Linux:
source phishing_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

## Verification

### Test Installation

1. **Start the application:**

   ```bash
   python main.py
   ```

2. **Open browser and go to:**
   `http://localhost:5000`

3. **Test API endpoint:**
   ```bash
   curl http://localhost:5000/health
   ```

### Expected Output

- Web interface loads successfully
- API returns health status
- No error messages in console

## Troubleshooting

### Common Installation Issues

#### Python Version Issues

- **Problem**: "Python 3.8+ required"
- **Solution**: Install Python 3.8 or higher

#### Dependencies Not Installing

- **Problem**: pip install fails
- **Solution**:
  ```bash
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

#### Port Already in Use

- **Problem**: "Port 5000 already in use"
- **Solution**:
  ```bash
  # Find process using port 5000
  # Windows: netstat -ano | findstr :5000
  # macOS/Linux: lsof -i :5000
  # Kill the process or use different port
  ```

#### Permission Issues

- **Problem**: "Permission denied" errors
- **Solution**: Run with appropriate permissions or use virtual environment

#### Missing Visual C++ (Windows)

- **Problem**: "Microsoft Visual C++ 14.0 is required"
- **Solution**: Install Microsoft C++ Build Tools

### Verification Steps

1. Check Python version: `python --version`
2. Verify dependencies: `pip list`
3. Test basic functionality: `python main.py`

## Post-Installation Configuration

### Configuration File

- Location: `config.py`
- Customize threshold values
- Adjust feature weights
- Configure logging settings

### Database Setup

- Database file: `phishing_detector.db`
- Created automatically on first run
- Located in application directory

### Logging Configuration

- Log files: `logs/` directory
- Daily rotation
- Configurable log levels

## Upgrading

### From Source

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
```

### Manual Update

- Download new version
- Replace files
- Run `pip install -r requirements.txt`

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate if active
deactivate
# Delete the entire directory
rm -rf phishing_env  # Linux/macOS
rmdir /s phishing_env  # Windows
```

### Remove Dependencies

```bash
pip uninstall -r requirements.txt -y
```

## Support

### Getting Help

- Check logs directory for error details
- Verify all dependencies are installed
- Ensure Python version is 3.8+
- Contact system administrator for assistance

```

```
