#!/usr/bin/env bash
# Render start script for PackCheck

set -o errexit  # Exit on error

echo "Starting PackCheck API..."
cd backend
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120 app:app
