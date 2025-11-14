#!/bin/bash

# Production start script
echo "Starting Phishing Detection System in production mode..."

# Set environment variables
export PYTHONUNBUFFERED=1
export FLASK_ENV=production

# Start the application with gunicorn
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --worker-class gevent --worker-connections 1000 wsgi:app