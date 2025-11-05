# PackCheck Installation Guide

This guide will help you set up and run the PackCheck application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.9 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **Node.js 16 or higher**
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify installation: `node --version`

3. **Tesseract OCR**
   - **Windows**: Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`
   - Verify installation: `tesseract --version`

4. **PostgreSQL** (Optional for production, SQLite used in development)
   - Download from [postgresql.org](https://www.postgresql.org/download/)

## Quick Start (Automated Setup)

### Windows
```bash
cd packcheck
setup.bat
```

### Linux/macOS
```bash
cd packcheck
chmod +x setup.sh
./setup.sh
```

## Manual Installation

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd packcheck/backend
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

4. **Install Python dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///packcheck.db
   DEBUG=True
   ```

6. **Create necessary directories**
   ```bash
   mkdir uploads
   ```

7. **Initialize database**
   ```bash
   python -c "from models.database import init_db; init_db()"
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

## Running the Application

### Start Backend Server

1. Navigate to backend directory
   ```bash
   cd backend
   ```

2. Activate virtual environment (if not already activated)
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

3. Run the Flask application
   ```bash
   python app.py
   ```

The backend API will be available at `http://localhost:5000`

### Start Frontend Development Server

1. Open a new terminal and navigate to frontend directory
   ```bash
   cd frontend
   ```

2. Start the development server
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## Accessing the Application

1. Open your web browser
2. Navigate to `http://localhost:3000`
3. You should see the PackCheck interface

## Tesseract Configuration

If Tesseract is not in your system PATH, you need to specify its location:

### Windows
Add to your `.env` file:
```
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Linux/macOS
Usually not needed, but if required:
```
TESSERACT_CMD=/usr/bin/tesseract
```

## Database Setup (Production)

For production use with PostgreSQL:

1. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE packcheck;
   CREATE USER packcheck_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE packcheck TO packcheck_user;
   ```

2. **Update .env file**
   ```
   DATABASE_URL=postgresql://packcheck_user:your_password@localhost/packcheck
   ```

3. **Initialize database tables**
   ```bash
   python -c "from models.database import init_db; init_db()"
   ```

## Troubleshooting

### Tesseract Not Found

**Error**: `TesseractNotFoundError`

**Solution**:
- Ensure Tesseract is installed
- Add Tesseract to system PATH
- Or specify TESSERACT_CMD in .env file

### Port Already in Use

**Error**: `Address already in use: 5000`

**Solution**:
- Change PORT in backend/.env
- Or kill the process using the port

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### CORS Errors

**Error**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**:
- Ensure backend is running
- Check CORS_ORIGINS in .env matches frontend URL

## Testing

Run the test suite:

```bash
cd tests
pytest
```

Run with coverage:
```bash
pytest --cov=backend
```

## Next Steps

- Read [API Documentation](API.md) for API endpoints
- Check [User Guide](USER_GUIDE.md) for usage instructions
- Review [Development Guide](DEVELOPMENT.md) for contributing

## Support

For issues and questions:
- Check existing issues on GitHub
- Create a new issue with detailed information
- Include error logs and system information
