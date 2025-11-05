# PackCheck: AI-Powered Food Label Verification System

PackCheck is an innovative food label verification system that combines OCR technology with FSSAI/WHO compliance verification, specifically designed for the Indian market and fitness enthusiasts.

## Key Features

- **AI-Powered Label Scanning**: Advanced OCR with Tesseract for extracting nutrition information from food labels
- **FSSAI Compliance Verification**: Real-time verification of "high protein" and other regulatory claims
- **Multi-Dimensional Confidence Scoring**: Reliability ratings across text clarity, regulatory compliance, and nutrient consistency
- **Fitness-Focused Personalization**: Protein optimization based on workout timing and muscle-building goals
- **Community Verification**: User-contributed corrections with dietitian validation

## Architecture

```
packcheck/
├── backend/          # Flask/FastAPI backend
│   ├── api/         # API endpoints
│   ├── models/      # Database models
│   ├── services/    # Business logic (OCR, FSSAI verification)
│   └── utils/       # Helper functions
├── frontend/        # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   └── public/
├── database/        # Database schemas and migrations
├── tests/          # Test suites
└── docs/           # Documentation
```

## Technology Stack

### Backend
- Python 3.9+
- Flask/FastAPI
- Tesseract OCR
- OpenCV for image preprocessing
- SQLAlchemy ORM
- PostgreSQL

### Frontend
- React 18+
- TypeScript
- Material-UI/Tailwind CSS
- Axios for API calls
- Camera integration for label scanning

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- Tesseract OCR
- PostgreSQL

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Environment Configuration

Create a `.env` file in the backend directory:

```
DATABASE_URL=postgresql://user:password@localhost/packcheck
SECRET_KEY=your-secret-key
FSSAI_API_KEY=your-fssai-api-key
```

## Usage

### Start Backend Server

```bash
cd backend
python app.py
```

### Start Frontend Development Server

```bash
cd frontend
npm start
```

## API Endpoints

- `POST /api/scan` - Upload and process food label image
- `GET /api/nutrition/{product_id}` - Get nutrition information
- `POST /api/verify/fssai` - Verify FSSAI compliance
- `GET /api/personalize` - Get personalized recommendations
- `POST /api/community/verify` - Submit community verification

## FSSAI Compliance Features

- Protein content verification (min 10g/serving for "high protein" claims)
- Veg/non-veg symbol recognition
- Expiry date validation
- Allergen declaration verification

## Development Roadmap

### Phase 1 (0-3 months)
- Core OCR functionality
- Basic FSSAI verification
- Simple frontend interface

### Phase 2 (3-6 months)
- Multi-dimensional confidence scoring
- Community verification system
- Fitness personalization features

### Phase 3 (6-12 months)
- WHO compliance integration
- Offline capability
- Mobile app development

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

MIT License

## Contact

For questions or support, please contact the development team.

---

Generated with PackCheck Vision: Regulatory-Compliant Personalization
