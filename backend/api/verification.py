"""
Verification API - FSSAI and WHO compliance verification endpoints
"""

from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from services.fssai_service import FSSAIService

verification_bp = Blueprint('verification', __name__)

# Initialize service
fssai_service = FSSAIService()

@verification_bp.route('/fssai', methods=['POST'])
def verify_fssai_compliance():
    """
    Verify FSSAI compliance for nutrition data

    Expects:
        - nutrition_facts: Dict of nutritional values
        - claims: List of claims made on packaging (optional)

    Returns:
        Comprehensive FSSAI verification results
    """
    data = request.get_json()

    if not data or 'nutrition_facts' not in data:
        return jsonify({'error': 'No nutrition data provided'}), 400

    nutrition_facts = data['nutrition_facts']
    claims = data.get('claims', [])

    try:
        verification = fssai_service.verify_all_claims(nutrition_facts, claims)

        return jsonify({
            'success': True,
            'verification': verification
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@verification_bp.route('/protein', methods=['POST'])
def verify_protein_claim():
    """
    Specifically verify protein-related claims

    Expects:
        - protein_content: Protein in grams
        - serving_size: Serving size in grams (optional)
        - claim: The specific claim made (optional)

    Returns:
        Protein claim verification
    """
    data = request.get_json()

    if not data or 'protein_content' not in data:
        return jsonify({'error': 'Protein content not provided'}), 400

    protein_content = data['protein_content']
    serving_size = data.get('serving_size', 100.0)
    claim = data.get('claim')

    try:
        verification = fssai_service.verify_protein_claim(
            protein_content,
            serving_size,
            claim
        )

        return jsonify({
            'success': True,
            'verification': verification
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@verification_bp.route('/expiry', methods=['POST'])
def verify_expiry_date():
    """
    Verify product expiry date

    Expects:
        - expiry_date: Expiry date string

    Returns:
        Expiry date verification
    """
    data = request.get_json()

    if not data or 'expiry_date' not in data:
        return jsonify({'error': 'Expiry date not provided'}), 400

    expiry_date = data['expiry_date']

    try:
        verification = fssai_service.verify_expiry_date(expiry_date)

        return jsonify({
            'success': True,
            'verification': verification
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@verification_bp.route('/allergens', methods=['POST'])
def detect_allergens():
    """
    Detect allergens in ingredient list

    Expects:
        - ingredients: List of ingredients

    Returns:
        Detected allergens
    """
    data = request.get_json()

    if not data or 'ingredients' not in data:
        return jsonify({'error': 'Ingredients not provided'}), 400

    ingredients = data['ingredients']

    try:
        allergen_info = fssai_service.detect_allergens(ingredients)

        return jsonify({
            'success': True,
            'allergen_info': allergen_info
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@verification_bp.route('/who', methods=['POST'])
def check_who_compliance():
    """
    Check compliance with WHO nutritional guidelines

    Expects:
        - nutrition_facts: Dict of nutritional values

    Returns:
        WHO compliance results
    """
    data = request.get_json()

    if not data or 'nutrition_facts' not in data:
        return jsonify({'error': 'No nutrition data provided'}), 400

    nutrition_facts = data['nutrition_facts']

    try:
        who_compliance = fssai_service._check_who_compliance(nutrition_facts)

        return jsonify({
            'success': True,
            'who_compliance': who_compliance
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@verification_bp.route('/standards', methods=['GET'])
def get_standards():
    """
    Get FSSAI and WHO standards for reference

    Returns:
        All regulatory standards
    """
    return jsonify({
        'success': True,
        'standards': {
            'fssai': fssai_service.FSSAI_STANDARDS,
            'who': fssai_service.WHO_STANDARDS
        }
    }), 200
