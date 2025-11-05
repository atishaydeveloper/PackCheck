"""
Scan API - Handle food label image uploads and processing
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from services.ocr_service import OCRService, validated_results
from services.fssai_service import FSSAIService

scan_bp = Blueprint('scan', __name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize services
ocr_service = OCRService()
fssai_service = FSSAIService()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@scan_bp.route('/', methods=['POST'])
def scan_label():
    """
    Main endpoint for scanning food labels

    Expects:
        - image file in multipart/form-data
        - optional: claims (list of claims made on packaging)

    Returns:
        - Extracted nutrition data
        - FSSAI compliance verification
        - Confidence scores
    """
    # Check if image is in request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, bmp'}), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Process image with OCR
        ocr_result = ocr_service.process_food_label(filepath)

        # Get claims from request if provided
        claims = request.form.getlist('claims') if 'claims' in request.form else []

        # Verify FSSAI compliance
        nutrition_data = ocr_result.get('nutrition_facts', {})
        fssai_verification = fssai_service.verify_all_claims(nutrition_data, claims)

        # Check allergens if ingredients found
        allergen_info = {}
        if ocr_result.get('ingredients'):
            allergen_info = fssai_service.detect_allergens(ocr_result['ingredients'])

        # Compile response
        response = {
            'success': True,
            'ocr_results': {
                'nutrition_facts': nutrition_data,
                'ingredients': ocr_result.get('ingredients', []),
                'raw_text': ocr_result.get('raw_text', ''),
                'confidence': ocr_result.get('confidence', {})
            },
            'fssai_verification': fssai_verification,
            'allergen_info': allergen_info,
            'overall_confidence': ocr_result.get('confidence', {}).get('overall', 0.0),
            'recommendation': _generate_recommendation(
                ocr_result.get('confidence', {}),
                fssai_verification
            )
        }

        # Clean up uploaded file
        os.remove(filepath)

        return jsonify(response), 200

    except Exception as e:
        # Clean up file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error processing image. Please ensure the label is clear and well-lit.'
        }), 500

@scan_bp.route('/batch', methods=['POST'])
def scan_multiple_labels():
    """
    Batch scanning endpoint for multiple labels

    Expects:
        - Multiple image files

    Returns:
        - Array of scan results
    """
    if 'images' not in request.files:
        return jsonify({'error': 'No images provided'}), 400

    files = request.files.getlist('images')
    results = []

    for file in files:
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                ocr_result = ocr_service.process_food_label(filepath)
                nutrition_data = ocr_result.get('nutrition_facts', {})
                fssai_verification = fssai_service.verify_all_claims(nutrition_data)

                results.append({
                    'filename': filename,
                    'success': True,
                    'nutrition_facts': nutrition_data,
                    'fssai_verification': fssai_verification,
                    'confidence': ocr_result.get('confidence', {})
                })

                os.remove(filepath)

            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'success': False,
                    'error': str(e)
                })

    return jsonify({
        'success': True,
        'total': len(files),
        'processed': len(results),
        'results': results
    }), 200

@scan_bp.route('/validate', methods=['POST'])
def validate_manual_entry():
    """
    Validate manually entered nutrition data against FSSAI standards

    Expects:
        - JSON with nutrition data
        - Optional: claims array

    Returns:
        - FSSAI verification results
    """
    data = request.get_json()

    if not data or 'nutrition_facts' not in data:
        return jsonify({'error': 'No nutrition data provided'}), 400

    nutrition_data = data['nutrition_facts']
    claims = data.get('claims', [])

    try:
        fssai_verification = fssai_service.verify_all_claims(nutrition_data, claims)

        return jsonify({
            'success': True,
            'verification': fssai_verification
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _generate_recommendation(confidence_scores: dict, fssai_verification: dict) -> dict:
    """Generate user-facing recommendation based on confidence and compliance"""
    overall_confidence = confidence_scores.get('overall', 0.0)
    compliance = fssai_verification.get('overall_compliance', True)
    trust_score = fssai_verification.get('trust_score', 1.0)

    recommendation = {
        'level': 'unknown',
        'message': '',
        'action': ''
    }

    # Determine recommendation level
    if overall_confidence >= 0.8 and compliance and trust_score >= 0.8:
        recommendation['level'] = 'high'
        recommendation['message'] = 'Data extraction reliable and claims verified'
        recommendation['action'] = 'Safe to use this nutritional information'

    elif overall_confidence >= 0.6 and trust_score >= 0.6:
        recommendation['level'] = 'medium'
        recommendation['message'] = 'Data extraction partially reliable'
        recommendation['action'] = 'Review the nutrition facts and verify manually if needed'

    else:
        recommendation['level'] = 'low'
        recommendation['message'] = 'Low confidence in data extraction or compliance issues detected'
        recommendation['action'] = 'Manual verification recommended or try rescanning with better lighting'

    # Add specific warnings
    if not compliance:
        recommendation['warnings'] = ['Some nutritional claims may not meet FSSAI standards']

    return recommendation
