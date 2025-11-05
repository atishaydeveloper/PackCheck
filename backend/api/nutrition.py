"""
Nutrition API - Manage nutrition data and product information
"""

from flask import Blueprint, request, jsonify

nutrition_bp = Blueprint('nutrition', __name__)

# In-memory storage for demo (would use database in production)
nutrition_database = {}

@nutrition_bp.route('/<product_id>', methods=['GET'])
def get_nutrition_info(product_id):
    """
    Get nutrition information for a specific product

    Args:
        product_id: Unique product identifier

    Returns:
        Nutrition information
    """
    if product_id in nutrition_database:
        return jsonify({
            'success': True,
            'product_id': product_id,
            'data': nutrition_database[product_id]
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404

@nutrition_bp.route('/store', methods=['POST'])
def store_nutrition_data():
    """
    Store scanned nutrition data for future reference

    Expects:
        - product_id
        - nutrition_facts
        - metadata (brand, name, etc.)

    Returns:
        Confirmation of storage
    """
    data = request.get_json()

    if not data or 'product_id' not in data or 'nutrition_facts' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    product_id = data['product_id']

    nutrition_database[product_id] = {
        'nutrition_facts': data['nutrition_facts'],
        'metadata': data.get('metadata', {}),
        'timestamp': data.get('timestamp'),
        'verified': data.get('verified', False)
    }

    return jsonify({
        'success': True,
        'message': 'Nutrition data stored successfully',
        'product_id': product_id
    }), 201

@nutrition_bp.route('/search', methods=['GET'])
def search_products():
    """
    Search for products by name or criteria

    Query params:
        - query: Search query
        - min_protein: Minimum protein content
        - max_sugar: Maximum sugar content

    Returns:
        List of matching products
    """
    query = request.args.get('query', '').lower()
    min_protein = float(request.args.get('min_protein', 0))
    max_sugar = float(request.args.get('max_sugar', 1000))

    results = []

    for product_id, data in nutrition_database.items():
        nutrition = data['nutrition_facts']
        metadata = data.get('metadata', {})

        # Check if matches search criteria
        protein = nutrition.get('protein', 0)
        sugar = nutrition.get('sugar', 0)

        name_match = query in metadata.get('name', '').lower() or query in metadata.get('brand', '').lower()

        if (query == '' or name_match) and protein >= min_protein and sugar <= max_sugar:
            results.append({
                'product_id': product_id,
                'name': metadata.get('name'),
                'brand': metadata.get('brand'),
                'nutrition_facts': nutrition
            })

    return jsonify({
        'success': True,
        'count': len(results),
        'results': results
    }), 200

@nutrition_bp.route('/compare', methods=['POST'])
def compare_products():
    """
    Compare nutrition facts of multiple products

    Expects:
        - product_ids: Array of product IDs to compare

    Returns:
        Comparison table
    """
    data = request.get_json()

    if not data or 'product_ids' not in data:
        return jsonify({'error': 'No product IDs provided'}), 400

    product_ids = data['product_ids']
    comparison = []

    for product_id in product_ids:
        if product_id in nutrition_database:
            product_data = nutrition_database[product_id]
            comparison.append({
                'product_id': product_id,
                'name': product_data.get('metadata', {}).get('name'),
                'nutrition_facts': product_data['nutrition_facts']
            })

    if not comparison:
        return jsonify({'error': 'No valid products found'}), 404

    # Calculate which product is best for different goals
    analysis = _analyze_comparison(comparison)

    return jsonify({
        'success': True,
        'products': comparison,
        'analysis': analysis
    }), 200

def _analyze_comparison(products):
    """Analyze products and determine best options for different goals"""
    analysis = {
        'highest_protein': None,
        'lowest_sugar': None,
        'lowest_fat': None,
        'best_for_fitness': None
    }

    highest_protein_val = 0
    lowest_sugar_val = float('inf')
    lowest_fat_val = float('inf')
    best_fitness_score = 0

    for product in products:
        nutrition = product['nutrition_facts']
        protein = nutrition.get('protein', 0)
        sugar = nutrition.get('sugar', float('inf'))
        fat = nutrition.get('fat', float('inf'))

        # Highest protein
        if protein > highest_protein_val:
            highest_protein_val = protein
            analysis['highest_protein'] = {
                'product_id': product['product_id'],
                'name': product['name'],
                'protein': protein
            }

        # Lowest sugar
        if sugar < lowest_sugar_val:
            lowest_sugar_val = sugar
            analysis['lowest_sugar'] = {
                'product_id': product['product_id'],
                'name': product['name'],
                'sugar': sugar
            }

        # Lowest fat
        if fat < lowest_fat_val:
            lowest_fat_val = fat
            analysis['lowest_fat'] = {
                'product_id': product['product_id'],
                'name': product['name'],
                'fat': fat
            }

        # Best for fitness (high protein, low sugar)
        fitness_score = protein - (sugar * 0.5)
        if fitness_score > best_fitness_score:
            best_fitness_score = fitness_score
            analysis['best_for_fitness'] = {
                'product_id': product['product_id'],
                'name': product['name'],
                'score': fitness_score
            }

    return analysis
