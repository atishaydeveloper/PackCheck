"""
FSSAI Compliance Verification Service
Implements regulatory verification for Indian food packaging standards
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import re

class FSSAIService:
    """Service for FSSAI regulatory compliance verification"""

    # FSSAI Standards
    FSSAI_STANDARDS = {
        'protein': {
            'high_protein_threshold': 10.0,  # g per serving
            'source_of_protein_threshold': 5.0,  # g per serving
            'unit': 'g'
        },
        'fiber': {
            'high_fiber_threshold': 6.0,  # g per serving
            'source_of_fiber_threshold': 3.0,  # g per serving
            'unit': 'g'
        },
        'sugar': {
            'low_sugar_threshold': 5.0,  # g per 100g
            'sugar_free_threshold': 0.5,  # g per 100g
            'unit': 'g'
        },
        'fat': {
            'low_fat_threshold': 3.0,  # g per 100g
            'fat_free_threshold': 0.5,  # g per 100g
            'unit': 'g'
        },
        'sodium': {
            'low_sodium_threshold': 120,  # mg per 100g
            'very_low_sodium_threshold': 40,  # mg per 100g
            'unit': 'mg'
        },
        'trans_fat': {
            'max_threshold': 2.2,  # g per serving
            'unit': 'g'
        }
    }

    # WHO Standards
    WHO_STANDARDS = {
        'daily_sodium_limit': 5000,  # mg/day
        'daily_sugar_limit': 25000,  # mg/day (25g)
        'daily_trans_fat_limit': 2200  # mg/day (2.2g)
    }

    def __init__(self):
        """Initialize FSSAI service"""
        self.verification_cache = {}

    def verify_protein_claim(self, protein_content: float,
                            serving_size: float = 100.0,
                            claim: str = None) -> Dict:
        """
        Verify protein-related claims against FSSAI standards

        Args:
            protein_content: Protein content in grams
            serving_size: Serving size in grams
            claim: The claim made on packaging (e.g., "high protein")

        Returns:
            Verification result with compliance status
        """
        # Normalize to per serving basis
        protein_per_serving = protein_content

        result = {
            'compliant': False,
            'actual_value': protein_per_serving,
            'claim': claim,
            'standard': None,
            'message': '',
            'trust_score': 0.0
        }

        if claim and 'high protein' in claim.lower():
            threshold = self.FSSAI_STANDARDS['protein']['high_protein_threshold']
            result['standard'] = f"FSSAI High Protein (≥{threshold}g per serving)"

            if protein_per_serving >= threshold:
                result['compliant'] = True
                result['trust_score'] = 1.0
                result['message'] = f"✓ Product meets FSSAI 'High Protein' standard with {protein_per_serving}g per serving"
            else:
                result['compliant'] = False
                result['trust_score'] = 0.3
                result['message'] = f"✗ Product claims 'High Protein' but contains only {protein_per_serving}g (requires ≥{threshold}g per serving)"

        elif claim and 'source of protein' in claim.lower():
            threshold = self.FSSAI_STANDARDS['protein']['source_of_protein_threshold']
            result['standard'] = f"FSSAI Source of Protein (≥{threshold}g per serving)"

            if protein_per_serving >= threshold:
                result['compliant'] = True
                result['trust_score'] = 1.0
                result['message'] = f"✓ Product meets FSSAI 'Source of Protein' standard"
            else:
                result['compliant'] = False
                result['trust_score'] = 0.3
                result['message'] = f"✗ Product claims 'Source of Protein' but contains insufficient protein"

        else:
            # No specific claim - just report value
            result['compliant'] = True  # No claim to verify
            result['trust_score'] = 0.8
            result['message'] = f"Product contains {protein_per_serving}g protein per serving (no claim made)"

            # Add helpful context
            high_threshold = self.FSSAI_STANDARDS['protein']['high_protein_threshold']
            if protein_per_serving >= high_threshold:
                result['message'] += f" - Qualifies as 'High Protein' by FSSAI standards"

        return result

    def verify_all_claims(self, nutrition_data: Dict, claims: List[str] = None) -> Dict:
        """
        Verify all nutritional claims against FSSAI standards

        Args:
            nutrition_data: Dictionary of nutritional values
            claims: List of claims made on packaging

        Returns:
            Comprehensive verification results
        """
        if claims is None:
            claims = []

        results = {
            'overall_compliance': True,
            'trust_score': 1.0,
            'verifications': {},
            'warnings': [],
            'recommendations': []
        }

        # Verify protein claims
        if 'protein' in nutrition_data:
            protein_claim = next((c for c in claims if 'protein' in c.lower()), None)
            protein_result = self.verify_protein_claim(
                nutrition_data['protein'],
                claim=protein_claim
            )
            results['verifications']['protein'] = protein_result

            if not protein_result['compliant']:
                results['overall_compliance'] = False
                results['trust_score'] *= 0.5

        # Verify sugar content
        if 'sugar' in nutrition_data:
            sugar_result = self._verify_sugar_content(nutrition_data['sugar'], claims)
            results['verifications']['sugar'] = sugar_result

            if not sugar_result['compliant']:
                results['overall_compliance'] = False
                results['trust_score'] *= 0.7

        # Verify fat content
        if 'fat' in nutrition_data:
            fat_result = self._verify_fat_content(nutrition_data['fat'], claims)
            results['verifications']['fat'] = fat_result

            if not fat_result['compliant']:
                results['overall_compliance'] = False
                results['trust_score'] *= 0.7

        # Verify sodium content
        if 'sodium' in nutrition_data:
            sodium_result = self._verify_sodium_content(nutrition_data['sodium'], claims)
            results['verifications']['sodium'] = sodium_result

            if not sodium_result['compliant']:
                results['overall_compliance'] = False
                results['trust_score'] *= 0.8

        # Check trans fat
        if 'trans_fat' in nutrition_data:
            trans_fat_result = self._verify_trans_fat(nutrition_data['trans_fat'])
            results['verifications']['trans_fat'] = trans_fat_result

            if not trans_fat_result['compliant']:
                results['overall_compliance'] = False
                results['trust_score'] *= 0.6
                results['warnings'].append("Trans fat exceeds FSSAI limits")

        # WHO compliance check
        who_compliance = self._check_who_compliance(nutrition_data)
        results['who_compliance'] = who_compliance

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(nutrition_data, results['verifications'])

        return results

    def _verify_sugar_content(self, sugar_content: float, claims: List[str]) -> Dict:
        """Verify sugar-related claims"""
        result = {
            'compliant': True,
            'actual_value': sugar_content,
            'message': '',
            'trust_score': 1.0
        }

        low_sugar_claim = any('low sugar' in c.lower() for c in claims)
        sugar_free_claim = any('sugar free' in c.lower() for c in claims)

        if low_sugar_claim:
            threshold = self.FSSAI_STANDARDS['sugar']['low_sugar_threshold']
            if sugar_content <= threshold:
                result['message'] = f"✓ Product meets 'Low Sugar' standard"
            else:
                result['compliant'] = False
                result['trust_score'] = 0.3
                result['message'] = f"✗ Product claims 'Low Sugar' but contains {sugar_content}g (requires ≤{threshold}g per 100g)"

        elif sugar_free_claim:
            threshold = self.FSSAI_STANDARDS['sugar']['sugar_free_threshold']
            if sugar_content <= threshold:
                result['message'] = f"✓ Product meets 'Sugar Free' standard"
            else:
                result['compliant'] = False
                result['trust_score'] = 0.2
                result['message'] = f"✗ Product claims 'Sugar Free' but contains {sugar_content}g"

        return result

    def _verify_fat_content(self, fat_content: float, claims: List[str]) -> Dict:
        """Verify fat-related claims"""
        result = {
            'compliant': True,
            'actual_value': fat_content,
            'message': '',
            'trust_score': 1.0
        }

        low_fat_claim = any('low fat' in c.lower() for c in claims)
        fat_free_claim = any('fat free' in c.lower() for c in claims)

        if low_fat_claim:
            threshold = self.FSSAI_STANDARDS['fat']['low_fat_threshold']
            if fat_content <= threshold:
                result['message'] = f"✓ Product meets 'Low Fat' standard"
            else:
                result['compliant'] = False
                result['trust_score'] = 0.3
                result['message'] = f"✗ Product claims 'Low Fat' but contains {fat_content}g"

        elif fat_free_claim:
            threshold = self.FSSAI_STANDARDS['fat']['fat_free_threshold']
            if fat_content <= threshold:
                result['message'] = f"✓ Product meets 'Fat Free' standard"
            else:
                result['compliant'] = False
                result['trust_score'] = 0.2
                result['message'] = f"✗ Product claims 'Fat Free' but contains {fat_content}g"

        return result

    def _verify_sodium_content(self, sodium_content: float, claims: List[str]) -> Dict:
        """Verify sodium-related claims"""
        result = {
            'compliant': True,
            'actual_value': sodium_content,
            'message': '',
            'trust_score': 1.0
        }

        low_sodium_claim = any('low sodium' in c.lower() for c in claims)

        if low_sodium_claim:
            threshold = self.FSSAI_STANDARDS['sodium']['low_sodium_threshold']
            if sodium_content <= threshold:
                result['message'] = f"✓ Product meets 'Low Sodium' standard"
            else:
                result['compliant'] = False
                result['trust_score'] = 0.3
                result['message'] = f"✗ Product claims 'Low Sodium' but contains {sodium_content}mg"

        return result

    def _verify_trans_fat(self, trans_fat_content: float) -> Dict:
        """Verify trans fat content against FSSAI limits"""
        threshold = self.FSSAI_STANDARDS['trans_fat']['max_threshold']

        result = {
            'compliant': trans_fat_content <= threshold,
            'actual_value': trans_fat_content,
            'message': '',
            'trust_score': 1.0 if trans_fat_content <= threshold else 0.3
        }

        if trans_fat_content <= threshold:
            result['message'] = f"✓ Trans fat within FSSAI limits ({trans_fat_content}g ≤ {threshold}g)"
        else:
            result['message'] = f"⚠ Trans fat exceeds FSSAI limits ({trans_fat_content}g > {threshold}g)"

        return result

    def _check_who_compliance(self, nutrition_data: Dict) -> Dict:
        """Check compliance with WHO guidelines"""
        compliance = {
            'compliant': True,
            'warnings': []
        }

        # Check sodium against WHO daily limit
        if 'sodium' in nutrition_data:
            sodium = nutrition_data['sodium']
            daily_limit = self.WHO_STANDARDS['daily_sodium_limit']

            # Assume per serving - calculate percentage of daily limit
            sodium_percentage = (sodium / daily_limit) * 100

            if sodium_percentage > 20:  # >20% of daily limit per serving
                compliance['warnings'].append(
                    f"High sodium content: {sodium}mg ({sodium_percentage:.1f}% of WHO daily limit)"
                )

        # Check sugar against WHO daily limit
        if 'sugar' in nutrition_data:
            sugar = nutrition_data['sugar'] * 1000  # Convert to mg
            daily_limit = self.WHO_STANDARDS['daily_sugar_limit']

            sugar_percentage = (sugar / daily_limit) * 100

            if sugar_percentage > 25:  # >25% of daily limit per serving
                compliance['warnings'].append(
                    f"High sugar content: {sugar/1000}g ({sugar_percentage:.1f}% of WHO daily limit)"
                )

        return compliance

    def _generate_recommendations(self, nutrition_data: Dict, verifications: Dict) -> List[str]:
        """Generate personalized recommendations based on nutrition data"""
        recommendations = []

        # Protein recommendations
        if 'protein' in nutrition_data:
            protein = nutrition_data['protein']
            if protein >= 10:
                recommendations.append("Good protein source for muscle building")
            elif protein >= 5:
                recommendations.append("Moderate protein content - consider supplementing")
            else:
                recommendations.append("Low protein content - not ideal for fitness goals")

        # Sugar warnings
        if 'sugar' in nutrition_data and nutrition_data['sugar'] > 10:
            recommendations.append("High sugar content - consume in moderation")

        # Trans fat warnings
        if 'trans_fat' in nutrition_data and nutrition_data['trans_fat'] > 0.5:
            recommendations.append("Contains trans fats - limit consumption")

        return recommendations

    def verify_expiry_date(self, expiry_date_str: str) -> Dict:
        """
        Verify expiry date validity

        Args:
            expiry_date_str: Expiry date string from label

        Returns:
            Verification result
        """
        result = {
            'valid': False,
            'expiry_date': None,
            'days_remaining': None,
            'message': ''
        }

        # Try to parse various date formats
        date_formats = [
            '%d/%m/%Y',
            '%d-%m-%Y',
            '%m/%Y',
            '%b %Y',
            '%B %Y'
        ]

        for fmt in date_formats:
            try:
                expiry_date = datetime.strptime(expiry_date_str.strip(), fmt)
                result['expiry_date'] = expiry_date.isoformat()

                today = datetime.now()
                days_remaining = (expiry_date - today).days

                result['days_remaining'] = days_remaining
                result['valid'] = days_remaining >= 0

                if days_remaining < 0:
                    result['message'] = f"⚠ Product expired {abs(days_remaining)} days ago"
                elif days_remaining < 30:
                    result['message'] = f"⚠ Product expires soon ({days_remaining} days remaining)"
                else:
                    result['message'] = f"✓ Product valid ({days_remaining} days remaining)"

                break
            except ValueError:
                continue

        if not result['expiry_date']:
            result['message'] = "Could not parse expiry date"

        return result

    def detect_allergens(self, ingredients: List[str]) -> Dict:
        """
        Detect common allergens in ingredient list

        Args:
            ingredients: List of ingredients

        Returns:
            Detected allergens
        """
        common_allergens = {
            'milk': ['milk', 'dairy', 'lactose', 'whey', 'casein'],
            'eggs': ['egg', 'albumin'],
            'peanuts': ['peanut', 'groundnut'],
            'tree_nuts': ['almond', 'cashew', 'walnut', 'pistachio'],
            'soy': ['soy', 'soya'],
            'wheat': ['wheat', 'gluten'],
            'fish': ['fish'],
            'shellfish': ['shrimp', 'crab', 'lobster']
        }

        detected_allergens = []

        ingredients_lower = ' '.join(ingredients).lower()

        for allergen, keywords in common_allergens.items():
            for keyword in keywords:
                if keyword in ingredients_lower:
                    detected_allergens.append(allergen)
                    break

        return {
            'allergens_detected': detected_allergens,
            'count': len(detected_allergens),
            'warning': len(detected_allergens) > 0
        }
