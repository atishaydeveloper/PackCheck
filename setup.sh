#!/bin/bash

# PackCheck Setup Script

echo "====================================="
echo "PackCheck Installation Setup"
echo "====================================="

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 is required but not installed. Aborting."; exit 1; }

# Check Node.js version
echo "Checking Node.js version..."
node --version || { echo "Node.js is required but not installed. Aborting."; exit 1; }

# Check Tesseract OCR
echo "Checking Tesseract OCR..."
tesseract --version || { echo "Warning: Tesseract OCR not found. Please install it separately."; }

echo ""
echo "====================================="
echo "Setting up Backend..."
echo "====================================="

# Setup backend
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit backend/.env with your configuration"
fi

# Create uploads directory
mkdir -p uploads

echo "Backend setup complete!"

cd ..

echo ""
echo "====================================="
echo "Setting up Frontend..."
echo "====================================="

# Setup frontend
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo "Frontend setup complete!"

cd ..

echo ""
echo "====================================="
echo "Setup Complete!"
echo "====================================="
echo ""
echo "To start the application:"
echo ""
echo "Backend:"
echo "  cd backend"
echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "  python app.py"
echo ""
echo "Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "The backend will run on http://localhost:5000"
echo "The frontend will run on http://localhost:3000"
echo ""
