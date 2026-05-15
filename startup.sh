#!/bin/bash
set -e

# Activate the virtual environment
source /antenv/bin/activate

# Start the app with uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
