#!/usr/bin/env bash
# Render build script for PackCheck

set -o errexit  # Exit on error

echo "Installing system dependencies..."
apt-get update
apt-get install -y tesseract-ocr tesseract-ocr-eng libgl1-mesa-glx libglib2.0-0

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"
