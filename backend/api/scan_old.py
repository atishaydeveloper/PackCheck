"""
Scan API - Handle food label image uploads and processing
Enhanced with Gemini AI
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
from services.gemini_service import GeminiService

scan_bp = Blueprint('scan', __name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize services
ocr_service = OCRService()
fssai_service = FSSAIService()

# Initialize Gemini AI (with fallback if API key not configured)
try:
    gemini_service = GeminiService()
    USE_GEMINI = True
    print("✓ Gemini AI initialized successfully")
except Exception as e:
    gemini_service = None
    USE_GEMINI = False
    print(f"⚠ Gemini AI not initialized: {e}")
    print("  Falling back to Tesseract OCR")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@scan_bp.route('/', methods=['POST'])
def scan_label():
    """
    Main endpoint for scanning food labels
    Uses Gemini AI if available, falls back to Tesseract OCR

    Expects:
        - image file in multipart/form-data
        - optional: use_ai (true/false) - force AI or OCR
        - optional: claims (list of claims made on packaging)

    Returns:
        - Extracted nutrition data
        - FSSAI compliance verification
        - AI-generated report (if Gemini is enabled)
        - Confidence scores
    """
    print(f"DEBUG: Received request - Files: {request.files.keys()}, Form: {request.form.keys()}")

    # Check if image is in request
    if 'image' not in request.files:
        print("DEBUG: No 'image' in request.files")
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    print(f"DEBUG: File received: {file.filename}")

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, bmp'}), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Check if user wants to force AI or OCR
        force_ai = request.form.get('use_ai', 'true').lower() == 'true'
        use_gemini_for_scan = USE_GEMINI and force_ai

        print(f"DEBUG: Using {'Gemini AI' if use_gemini_for_scan else 'Tesseract OCR'} for extraction")

        # Extract nutrition data
        if use_gemini_for_scan:
            # Use Gemini AI for extraction
            gemini_result = gemini_service.extract_nutrition_from_image(filepath)

            if gemini_result['success']:
                extracted_data = gemini_result['data']
                nutrition_data = extracted_data.get('nutrition_facts', {})
                ingredients = extracted_data.get('ingredients', [])
                claims = extracted_data.get('claims', [])

                # Add user-provided claims
                if 'claims' in request.form:
                    user_claims = request.form.getlist('claims')
                    claims.extend(user_claims)

                extraction_source = 'gemini-ai'
                extraction_confidence = 0.95  # Gemini typically high confidence
            else:
                # Gemini failed, fall back to Tesseract
                print(f"DEBUG: Gemini extraction failed: {gemini_result.get('error')}")
                ocr_result = ocr_service.process_food_label(filepath)
                nutrition_data = ocr_result.get('nutrition_facts', {})
                ingredients = ocr_result.get('ingredients', [])
                claims = request.form.getlist('claims') if 'claims' in request.form else []
                extraction_source = 'tesseract-ocr'
                extraction_confidence = ocr_result.get('confidence', {}).get('overall', 0.0)
        else:
            # Use traditional Tesseract OCR
            ocr_result = ocr_service.process_food_label(filepath)
            nutrition_data = ocr_result.get('nutrition_facts', {})
            ingredients = ocr_result.get('ingredients', [])
            claims = request.form.getlist('claims') if 'claims' in request.form else []
            extraction_source = 'tesseract-ocr'
            extraction_confidence = ocr_result.get('confidence', {}).get('overall', 0.0)

        # Verify FSSAI compliance
        fssai_verification = fssai_service.verify_all_claims(nutrition_data, claims)

        # Check allergens if ingredients found
        allergen_info = {}
        if ingredients:
            allergen_info = fssai_service.detect_allergens(ingredients)

        # Generate AI report if Gemini is available
        ai_report = None
        if USE_GEMINI:
            try:
                report_result = gemini_service.generate_comprehensive_report(
                    nutrition_data,
                    fssai_verification
                )
                if report_result['success']:
                    ai_report = report_result['report']
            except Exception as e:
                print(f"DEBUG: AI report generation failed: {e}")

        # Compile response
        response = {
            'success': True,
            'extraction_source': extraction_source,
            'ai_enabled': USE_GEMINI,
            'nutrition_data': nutrition_data,
            'ingredients': ingredients,
            'claims_detected': claims,
            'fssai_verification': fssai_verification,
            'allergen_info': allergen_info,
            'confidence': extraction_confidence,
            'ai_report': ai_report,
            'recommendation': _generate_recommendation(
                extraction_confidence,
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

        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error processing image. Please ensure the label is clear and well-lit.'
        }), 500

@scan_bp.route('/ai-report', methods=['POST'])
def generate_ai_report():
    """
    Generate AI report for already extracted nutrition data

    Expects:
        - JSON with nutrition_data, fssai_verification, user_profile (optional)

    Returns:
        - AI-generated comprehensive report
    """
    if not USE_GEMINI:
        return jsonify({
            'success': False,
            'error': 'Gemini AI not configured. Please add GEMINI_API_KEY to environment.'
        }), 503

    data = request.get_json()

    if not data or 'nutrition_data' not in data:
        return jsonify({'error': 'Nutrition data required'}), 400

    try:
        report_result = gemini_service.generate_comprehensive_report(
            data['nutrition_data'],
            data.get('fssai_verification', {}),
            data.get('user_profile')
        )

        return jsonify(report_result), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scan_bp.route('/ai-recommend', methods=['POST'])
def get_ai_recommendation():
    """
    Get personalized AI recommendation

    Expects:
        - JSON with nutrition_data, user_profile, workout_timing

    Returns:
        - AI-generated personalized recommendation
    """
    if not USE_GEMINI:
        return jsonify({
            'success': False,
            'error': 'Gemini AI not configured'
        }), 503

    data = request.get_json()

    if not data or 'nutrition_data' not in data or 'user_profile' not in data:
        return jsonify({'error': 'nutrition_data and user_profile required'}), 400

    try:
        recommendation = gemini_service.generate_personalized_recommendation(
            data['nutrition_data'],
            data['user_profile'],
            data.get('workout_timing', 'general')
        )

        return jsonify(recommendation), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scan_bp.route('/ai-compare', methods=['POST'])
def compare_products_ai():
    """
    Compare products using AI

    Expects:
        - JSON with products array

    Returns:
        - AI-generated comparison
    """
    if not USE_GEMINI:
        return jsonify({
            'success': False,
            'error': 'Gemini AI not configured'
        }), 503

    data = request.get_json()

    if not data or 'products' not in data:
        return jsonify({'error': 'Products array required'}), 400

    try:
        comparison = gemini_service.compare_products_ai(data['products'])
        return jsonify(comparison), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scan_bp.route('/ai-ingredients', methods=['POST'])
def analyze_ingredients():
    """
    Analyze ingredient safety using AI

    Expects:
        - JSON with ingredients array

    Returns:
        - AI safety analysis
    """
    if not USE_GEMINI:
        return jsonify({
            'success': False,
            'error': 'Gemini AI not configured'
        }), 503

    data = request.get_json()

    if not data or 'ingredients' not in data:
        return jsonify({'error': 'Ingredients array required'}), 400

    try:
        analysis = gemini_service.analyze_ingredients_safety(data['ingredients'])
        return jsonify(analysis), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scan_bp.route('/ai-ask', methods=['POST'])
def ask_nutrition_question():
    """
    Ask nutrition questions to AI

    Expects:
        - JSON with question and optional context

    Returns:
        - AI answer
    """
    if not USE_GEMINI:
        return jsonify({
            'success': False,
            'error': 'Gemini AI not configured'
        }), 503

    data = request.get_json()

    if not data or 'question' not in data:
        return jsonify({'error': 'Question required'}), 400

    try:
        answer = gemini_service.answer_nutrition_question(
            data['question'],
            data.get('context')
        )
        return jsonify(answer), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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

def _generate_recommendation(confidence: float, fssai_verification: dict) -> dict:
    """Generate user-facing recommendation based on confidence and compliance"""
    compliance = fssai_verification.get('overall_compliance', True)
    trust_score = fssai_verification.get('trust_score', 1.0)

    recommendation = {
        'level': 'unknown',
        'message': '',
        'action': ''
    }

    # Determine recommendation level
    if confidence >= 0.8 and compliance and trust_score >= 0.8:
        recommendation['level'] = 'high'
        recommendation['message'] = 'Data extraction reliable and claims verified'
        recommendation['action'] = 'Safe to use this nutritional information'

    elif confidence >= 0.6 and trust_score >= 0.6:
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
