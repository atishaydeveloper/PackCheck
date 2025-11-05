"""
Unit tests for OCR Service
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / 'backend'))

from services.ocr_service import OCRService

class TestOCRService:
    """Test OCR Service functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        self.ocr_service = OCRService()

    def test_ocr_service_initialization(self):
        """Test OCR service initializes correctly"""
        assert self.ocr_service is not None
        assert self.ocr_service.tesseract_config is not None

    def test_extract_nutrition_facts(self):
        """Test nutrition facts extraction from text"""
        # Mock nutrition table image would be here
        # For now, testing the pattern matching
        import numpy as np

        # Create a dummy image
        dummy_image = np.zeros((100, 100), dtype=np.uint8)

        # This would fail without actual text, but tests the method exists
        result = self.ocr_service._extract_nutrition_facts(dummy_image)
        assert isinstance(result, dict)

    def test_confidence_scoring(self):
        """Test multi-dimensional confidence scoring"""
        extracted_data = {
            'nutrition_table': {
                'protein': 20.0,
                'carbohydrates': 30.0,
                'fat': 10.0
            }
        }

        import numpy as np
        dummy_image = np.zeros((100, 100), dtype=np.uint8)

        confidence = self.ocr_service._multi_dimensional_scoring(
            extracted_data,
            dummy_image
        )

        assert isinstance(confidence, dict)
        assert 'overall' in confidence
        assert 0 <= confidence['overall'] <= 1

    def test_text_clarity_calculation(self):
        """Test text clarity score calculation"""
        import numpy as np

        # Create a test image
        image = np.random.randint(0, 255, (200, 200), dtype=np.uint8)

        extracted_data = {
            'nutrition_table': {
                'protein': 15.0
            }
        }

        clarity_score = self.ocr_service._calculate_text_clarity(image, extracted_data)

        assert isinstance(clarity_score, float)
        assert 0 <= clarity_score <= 1

    def test_compliance_score_calculation(self):
        """Test compliance score calculation"""
        extracted_data = {
            'nutrition_table': {
                'protein': 20.0,
                'carbohydrates': 30.0,
                'fat': 10.0,
                'calories': 300
            }
        }

        compliance_score = self.ocr_service._calculate_compliance_score(extracted_data)

        assert isinstance(compliance_score, float)
        assert 0 <= compliance_score <= 1

    def test_consistency_score_calculation(self):
        """Test nutrient consistency score"""
        extracted_data = {
            'nutrition_table': {
                'protein': 20.0,
                'carbohydrates': 30.0,
                'fat': 10.0
            }
        }

        consistency_score = self.ocr_service._calculate_consistency_score(extracted_data)

        assert isinstance(consistency_score, float)
        assert 0 <= consistency_score <= 1

    def test_consistency_score_invalid_data(self):
        """Test consistency score with unrealistic values"""
        extracted_data = {
            'nutrition_table': {
                'protein': 150.0,  # Unrealistically high
                'carbohydrates': 200.0,
                'fat': 100.0
            }
        }

        consistency_score = self.ocr_service._calculate_consistency_score(extracted_data)

        # Should be lower due to unrealistic values
        assert consistency_score < 1.0

if __name__ == '__main__':
    pytest.main([__file__])
