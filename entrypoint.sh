#!/bin/bash
set -e

echo "--- Sierra6 Stash Manager Startup ---"

# 1. Navigate to the app directory
cd /app

# 2. Start the Python Flask server
# We use 'exec' so that Python becomes PID 1
echo "Starting server..."
exec python3 server.py