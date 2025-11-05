"""
Community API - Community verification and contributions
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

community_bp = Blueprint('community', __name__)

# Community data storage (would use database in production)
community_verifications = {}
community_corrections = []

@community_bp.route('/verify', methods=['POST'])
def submit_community_verification():
    """
    Submit community verification for a scanned label

    Expects:
        - product_id
        - user_id
        - verification_type: (confirm, correct, flag)
        - data: Corrected or verified data
        - confidence: User confidence in their submission

    Returns:
        Verification submission confirmation
    """
    data = request.get_json()

    if not data or 'product_id' not in data or 'user_id' not in data:
        return jsonify({'error': 'Product ID and User ID required'}), 400

    product_id = data['product_id']
    verification = {
        'verification_id': f"cv_{len(community_corrections) + 1}",
        'product_id': product_id,
        'user_id': data['user_id'],
        'verification_type': data.get('verification_type', 'confirm'),
        'data': data.get('data', {}),
        'confidence': data.get('confidence', 'medium'),
        'timestamp': datetime.now().isoformat(),
        'status': 'pending',  # pending, approved, rejected
        'dietitian_verified': False
    }

    community_corrections.append(verification)

    # Update product verification count
    if product_id not in community_verifications:
        community_verifications[product_id] = {
            'confirmations': 0,
            'corrections': 0,
            'flags': 0,
            'verified_data': None
        }

    if verification['verification_type'] == 'confirm':
        community_verifications[product_id]['confirmations'] += 1
    elif verification['verification_type'] == 'correct':
        community_verifications[product_id]['corrections'] += 1
    else:  # flag
        community_verifications[product_id]['flags'] += 1

    return jsonify({
        'success': True,
        'verification': verification,
        'message': 'Thank you for your contribution! A dietitian will review your submission.'
    }), 201

@community_bp.route('/verify/<product_id>', methods=['GET'])
def get_community_verifications(product_id):
    """
    Get community verifications for a product

    Returns:
        Community verification statistics
    """
    if product_id in community_verifications:
        return jsonify({
            'success': True,
            'product_id': product_id,
            'verifications': community_verifications[product_id]
        }), 200
    else:
        return jsonify({
            'success': True,
            'product_id': product_id,
            'verifications': {
                'confirmations': 0,
                'corrections': 0,
                'flags': 0,
                'verified_data': None
            }
        }), 200

@community_bp.route('/corrections', methods=['GET'])
def get_pending_corrections():
    """
    Get pending community corrections (for dietitian review)

    Query params:
        - status: pending, approved, rejected

    Returns:
        List of corrections
    """
    status = request.args.get('status', 'pending')

    filtered_corrections = [
        c for c in community_corrections
        if c['status'] == status
    ]

    return jsonify({
        'success': True,
        'count': len(filtered_corrections),
        'corrections': filtered_corrections
    }), 200

@community_bp.route('/corrections/<verification_id>/approve', methods=['POST'])
def approve_correction(verification_id):
    """
    Approve a community correction (dietitian action)

    Expects:
        - dietitian_id
        - notes (optional)

    Returns:
        Approval confirmation
    """
    data = request.get_json()

    if not data or 'dietitian_id' not in data:
        return jsonify({'error': 'Dietitian ID required'}), 400

    # Find correction
    correction = next((c for c in community_corrections if c['verification_id'] == verification_id), None)

    if not correction:
        return jsonify({'error': 'Verification not found'}), 404

    # Approve correction
    correction['status'] = 'approved'
    correction['dietitian_verified'] = True
    correction['dietitian_id'] = data['dietitian_id']
    correction['dietitian_notes'] = data.get('notes', '')
    correction['reviewed_at'] = datetime.now().isoformat()

    # Update product verified data
    product_id = correction['product_id']
    if product_id in community_verifications:
        community_verifications[product_id]['verified_data'] = correction['data']

    return jsonify({
        'success': True,
        'message': 'Correction approved',
        'verification': correction
    }), 200

@community_bp.route('/corrections/<verification_id>/reject', methods=['POST'])
def reject_correction(verification_id):
    """
    Reject a community correction (dietitian action)

    Expects:
        - dietitian_id
        - reason

    Returns:
        Rejection confirmation
    """
    data = request.get_json()

    if not data or 'dietitian_id' not in data or 'reason' not in data:
        return jsonify({'error': 'Dietitian ID and reason required'}), 400

    # Find correction
    correction = next((c for c in community_corrections if c['verification_id'] == verification_id), None)

    if not correction:
        return jsonify({'error': 'Verification not found'}), 404

    # Reject correction
    correction['status'] = 'rejected'
    correction['dietitian_id'] = data['dietitian_id']
    correction['rejection_reason'] = data['reason']
    correction['reviewed_at'] = datetime.now().isoformat()

    return jsonify({
        'success': True,
        'message': 'Correction rejected',
        'verification': correction
    }), 200

@community_bp.route('/leaderboard', methods=['GET'])
def get_community_leaderboard():
    """
    Get community contributors leaderboard

    Returns:
        Top contributors
    """
    # Count contributions per user
    user_contributions = {}

    for correction in community_corrections:
        user_id = correction['user_id']
        if user_id not in user_contributions:
            user_contributions[user_id] = {
                'user_id': user_id,
                'total': 0,
                'approved': 0,
                'pending': 0,
                'rejected': 0
            }

        user_contributions[user_id]['total'] += 1

        if correction['status'] == 'approved':
            user_contributions[user_id]['approved'] += 1
        elif correction['status'] == 'pending':
            user_contributions[user_id]['pending'] += 1
        else:
            user_contributions[user_id]['rejected'] += 1

    # Sort by approved contributions
    leaderboard = sorted(
        user_contributions.values(),
        key=lambda x: x['approved'],
        reverse=True
    )[:10]  # Top 10

    return jsonify({
        'success': True,
        'leaderboard': leaderboard
    }), 200

@community_bp.route('/badge', methods=['GET'])
def check_community_badge():
    """
    Check if a product has community verified badge

    Query params:
        - product_id

    Returns:
        Badge status
    """
    product_id = request.args.get('product_id')

    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400

    badge_status = {
        'has_badge': False,
        'badge_level': None,
        'verification_count': 0,
        'last_verified': None
    }

    if product_id in community_verifications:
        verif = community_verifications[product_id]
        confirmations = verif['confirmations']

        # Award badge based on confirmations
        if confirmations >= 10:
            badge_status['has_badge'] = True
            badge_status['badge_level'] = 'gold'
        elif confirmations >= 5:
            badge_status['has_badge'] = True
            badge_status['badge_level'] = 'silver'
        elif confirmations >= 3:
            badge_status['has_badge'] = True
            badge_status['badge_level'] = 'bronze'

        badge_status['verification_count'] = confirmations

        # Get last verification timestamp
        product_corrections = [
            c for c in community_corrections
            if c['product_id'] == product_id and c['verification_type'] == 'confirm'
        ]

        if product_corrections:
            latest = max(product_corrections, key=lambda x: x['timestamp'])
            badge_status['last_verified'] = latest['timestamp']

    return jsonify({
        'success': True,
        'product_id': product_id,
        'badge': badge_status
    }), 200
