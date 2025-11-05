"""
Unit tests for FSSAI Verification Service
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / 'backend'))

from services.fssai_service import FSSAIService

class TestFSSAIService:
    """Test FSSAI Verification Service"""

    def setup_method(self):
        """Setup test fixtures"""
        self.fssai_service = FSSAIService()

    def test_fssai_service_initialization(self):
        """Test FSSAI service initializes correctly"""
        assert self.fssai_service is not None
        assert self.fssai_service.FSSAI_STANDARDS is not None
        assert self.fssai_service.WHO_STANDARDS is not None

    def test_verify_protein_claim_high_protein_compliant(self):
        """Test verification of compliant high protein claim"""
        result = self.fssai_service.verify_protein_claim(
            protein_content=15.0,
            serving_size=100.0,
            claim="high protein"
        )

        assert result['compliant'] is True
        assert result['trust_score'] == 1.0
        assert 'High Protein' in result['standard']

    def test_verify_protein_claim_high_protein_non_compliant(self):
        """Test verification of non-compliant high protein claim"""
        result = self.fssai_service.verify_protein_claim(
            protein_content=8.0,
            serving_size=100.0,
            claim="high protein"
        )

        assert result['compliant'] is False
        assert result['trust_score'] < 1.0

    def test_verify_protein_claim_no_claim(self):
        """Test protein verification with no claim"""
        result = self.fssai_service.verify_protein_claim(
            protein_content=12.0,
            serving_size=100.0,
            claim=None
        )

        assert result['compliant'] is True
        assert result['trust_score'] > 0

    def test_verify_all_claims_compliant(self):
        """Test verification of all claims with compliant data"""
        nutrition_data = {
            'protein': 15.0,
            'sugar': 4.0,
            'fat': 2.0,
            'sodium': 100
        }

        claims = ['high protein', 'low sugar', 'low fat']

        result = self.fssai_service.verify_all_claims(nutrition_data, claims)

        assert isinstance(result, dict)
        assert 'overall_compliance' in result
        assert 'verifications' in result

    def test_verify_sugar_content_low_sugar(self):
        """Test low sugar claim verification"""
        result = self.fssai_service._verify_sugar_content(4.0, ['low sugar'])

        assert result['compliant'] is True
        assert result['trust_score'] == 1.0

    def test_verify_fat_content_low_fat(self):
        """Test low fat claim verification"""
        result = self.fssai_service._verify_fat_content(2.5, ['low fat'])

        assert result['compliant'] is True
        assert result['trust_score'] == 1.0

    def test_verify_trans_fat_compliant(self):
        """Test trans fat verification within limits"""
        result = self.fssai_service._verify_trans_fat(1.5)

        assert result['compliant'] is True
        assert result['trust_score'] == 1.0

    def test_verify_trans_fat_non_compliant(self):
        """Test trans fat verification exceeding limits"""
        result = self.fssai_service._verify_trans_fat(3.0)

        assert result['compliant'] is False
        assert result['trust_score'] < 1.0

    def test_check_who_compliance(self):
        """Test WHO compliance checking"""
        nutrition_data = {
            'sodium': 2000,  # mg
            'sugar': 15.0    # g
        }

        result = self.fssai_service._check_who_compliance(nutrition_data)

        assert isinstance(result, dict)
        assert 'compliant' in result
        assert 'warnings' in result

    def test_verify_expiry_date_valid(self):
        """Test expiry date verification for valid date"""
        from datetime import datetime, timedelta

        future_date = datetime.now() + timedelta(days=30)
        expiry_str = future_date.strftime('%d/%m/%Y')

        result = self.fssai_service.verify_expiry_date(expiry_str)

        assert result['valid'] is True
        assert result['days_remaining'] > 0

    def test_verify_expiry_date_expired(self):
        """Test expiry date verification for expired date"""
        from datetime import datetime, timedelta

        past_date = datetime.now() - timedelta(days=30)
        expiry_str = past_date.strftime('%d/%m/%Y')

        result = self.fssai_service.verify_expiry_date(expiry_str)

        assert result['valid'] is False
        assert result['days_remaining'] < 0

    def test_detect_allergens(self):
        """Test allergen detection"""
        ingredients = [
            'wheat flour',
            'milk powder',
            'peanuts',
            'sugar',
            'salt'
        ]

        result = self.fssai_service.detect_allergens(ingredients)

        assert isinstance(result, dict)
        assert 'allergens_detected' in result
        assert len(result['allergens_detected']) > 0
        assert 'wheat' in result['allergens_detected']
        assert 'milk' in result['allergens_detected']
        assert 'peanuts' in result['allergens_detected']

    def test_detect_allergens_none(self):
        """Test allergen detection with no allergens"""
        ingredients = [
            'rice',
            'sugar',
            'salt'
        ]

        result = self.fssai_service.detect_allergens(ingredients)

        assert len(result['allergens_detected']) == 0
        assert result['warning'] is False

    def test_generate_recommendations(self):
        """Test recommendation generation"""
        nutrition_data = {
            'protein': 20.0,
            'sugar': 5.0,
            'trans_fat': 0.3
        }

        verifications = {}

        recommendations = self.fssai_service._generate_recommendations(
            nutrition_data,
            verifications
        )

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

if __name__ == '__main__':
    pytest.main([__file__])
