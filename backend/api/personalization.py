"""
Personalization API - Fitness-focused personalized recommendations
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

personalization_bp = Blueprint('personalization', __name__)

# User profiles (would use database in production)
user_profiles = {}

@personalization_bp.route('/profile', methods=['POST'])
def create_user_profile():
    """
    Create or update user profile for personalization

    Expects:
        - user_id
        - fitness_goal: (muscle_building, weight_loss, maintenance)
        - workout_schedule: Dict with workout days and times
        - dietary_preferences: Dict with preferences
        - body_metrics: weight, height, age, gender

    Returns:
        Created profile
    """
    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({'error': 'User ID required'}), 400

    user_id = data['user_id']

    user_profiles[user_id] = {
        'user_id': user_id,
        'fitness_goal': data.get('fitness_goal', 'maintenance'),
        'workout_schedule': data.get('workout_schedule', {}),
        'dietary_preferences': data.get('dietary_preferences', {}),
        'body_metrics': data.get('body_metrics', {}),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    # Calculate personalized targets
    targets = _calculate_nutrition_targets(user_profiles[user_id])
    user_profiles[user_id]['targets'] = targets

    return jsonify({
        'success': True,
        'profile': user_profiles[user_id]
    }), 201

@personalization_bp.route('/profile/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    """Get user profile"""
    if user_id in user_profiles:
        return jsonify({
            'success': True,
            'profile': user_profiles[user_id]
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Profile not found'
        }), 404

@personalization_bp.route('/recommend', methods=['POST'])
def get_personalized_recommendations():
    """
    Get personalized recommendations for a product

    Expects:
        - user_id
        - nutrition_facts
        - workout_timing: (pre_workout, post_workout, recovery, general)

    Returns:
        Personalized recommendations
    """
    data = request.get_json()

    if not data or 'user_id' not in data or 'nutrition_facts' not in data:
        return jsonify({'error': 'User ID and nutrition facts required'}), 400

    user_id = data['user_id']
    nutrition_facts = data['nutrition_facts']
    workout_timing = data.get('workout_timing', 'general')

    if user_id not in user_profiles:
        return jsonify({'error': 'User profile not found'}), 404

    profile = user_profiles[user_id]

    # Generate personalized recommendations
    recommendations = _generate_personalized_recommendations(
        profile,
        nutrition_facts,
        workout_timing
    )

    return jsonify({
        'success': True,
        'recommendations': recommendations
    }), 200

@personalization_bp.route('/analyze', methods=['POST'])
def analyze_for_fitness_goal():
    """
    Analyze product suitability for specific fitness goals

    Expects:
        - nutrition_facts
        - fitness_goal
        - workout_timing (optional)

    Returns:
        Detailed fitness-focused analysis
    """
    data = request.get_json()

    if not data or 'nutrition_facts' not in data:
        return jsonify({'error': 'Nutrition facts required'}), 400

    nutrition_facts = data['nutrition_facts']
    fitness_goal = data.get('fitness_goal', 'muscle_building')
    workout_timing = data.get('workout_timing', 'general')

    analysis = _analyze_for_fitness(nutrition_facts, fitness_goal, workout_timing)

    return jsonify({
        'success': True,
        'analysis': analysis
    }), 200

@personalization_bp.route('/timing', methods=['POST'])
def get_timing_recommendation():
    """
    Get workout timing-specific recommendations

    Expects:
        - nutrition_facts
        - current_time (optional)
        - next_workout_time (optional)

    Returns:
        Timing-based recommendations
    """
    data = request.get_json()

    if not data or 'nutrition_facts' not in data:
        return jsonify({'error': 'Nutrition facts required'}), 400

    nutrition_facts = data['nutrition_facts']

    # Determine optimal consumption timing
    timing_rec = _determine_optimal_timing(nutrition_facts)

    return jsonify({
        'success': True,
        'timing_recommendation': timing_rec
    }), 200

def _calculate_nutrition_targets(profile):
    """Calculate personalized nutrition targets based on profile"""
    body_metrics = profile.get('body_metrics', {})
    fitness_goal = profile.get('fitness_goal', 'maintenance')

    weight = body_metrics.get('weight', 70)  # kg
    height = body_metrics.get('height', 170)  # cm
    age = body_metrics.get('age', 25)
    gender = body_metrics.get('gender', 'male')

    # Calculate BMR (Basal Metabolic Rate) using Mifflin-St Jeor equation
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Adjust for activity level (assuming moderate activity)
    tdee = bmr * 1.55

    # Adjust for fitness goal
    if fitness_goal == 'muscle_building':
        calories = tdee + 300  # Surplus
        protein_per_kg = 2.0  # 2g per kg bodyweight
        carb_percentage = 0.40
        fat_percentage = 0.25
    elif fitness_goal == 'weight_loss':
        calories = tdee - 500  # Deficit
        protein_per_kg = 1.8
        carb_percentage = 0.30
        fat_percentage = 0.30
    else:  # maintenance
        calories = tdee
        protein_per_kg = 1.6
        carb_percentage = 0.40
        fat_percentage = 0.30

    protein_target = weight * protein_per_kg
    carb_target = (calories * carb_percentage) / 4  # 4 cal per g
    fat_target = (calories * fat_percentage) / 9  # 9 cal per g

    return {
        'daily_calories': round(calories),
        'daily_protein': round(protein_target),
        'daily_carbs': round(carb_target),
        'daily_fat': round(fat_target),
        'per_meal': {
            'protein': round(protein_target / 4),  # 4 meals
            'carbs': round(carb_target / 4),
            'fat': round(fat_target / 4)
        }
    }

def _generate_personalized_recommendations(profile, nutrition_facts, workout_timing):
    """Generate personalized recommendations based on user profile"""
    targets = profile.get('targets', {})
    fitness_goal = profile.get('fitness_goal', 'maintenance')

    protein = nutrition_facts.get('protein', 0)
    carbs = nutrition_facts.get('carbohydrates', 0)
    fat = nutrition_facts.get('fat', 0)
    sugar = nutrition_facts.get('sugar', 0)

    recommendations = {
        'suitability_score': 0.0,
        'messages': [],
        'timing': '',
        'alternatives': []
    }

    per_meal_protein = targets.get('per_meal', {}).get('protein', 25)

    # Evaluate based on workout timing
    if workout_timing == 'pre_workout':
        # Pre-workout needs moderate carbs, low fat, moderate protein
        if carbs >= 20 and fat < 5 and protein >= 10:
            recommendations['suitability_score'] = 0.9
            recommendations['messages'].append('Excellent pre-workout option')
        elif carbs >= 15:
            recommendations['suitability_score'] = 0.7
            recommendations['messages'].append('Good pre-workout carb source')
        else:
            recommendations['suitability_score'] = 0.4
            recommendations['messages'].append('May not provide enough energy for workout')

        recommendations['timing'] = 'Consume 30-60 minutes before workout'

    elif workout_timing == 'post_workout':
        # Post-workout needs high protein, moderate-high carbs
        if protein >= per_meal_protein and carbs >= 25:
            recommendations['suitability_score'] = 1.0
            recommendations['messages'].append('Perfect post-workout recovery food')
        elif protein >= per_meal_protein * 0.7:
            recommendations['suitability_score'] = 0.75
            recommendations['messages'].append('Good protein source for recovery')
        else:
            recommendations['suitability_score'] = 0.5
            recommendations['messages'].append(f'Protein content low for optimal recovery (need {per_meal_protein}g)')

        recommendations['timing'] = 'Consume within 30-45 minutes post-workout'

    elif workout_timing == 'recovery':
        # Recovery needs high protein, low sugar
        if protein >= 20 and sugar < 10:
            recommendations['suitability_score'] = 0.9
            recommendations['messages'].append('Excellent for muscle recovery')
        elif protein >= 15:
            recommendations['suitability_score'] = 0.7
            recommendations['messages'].append('Good recovery snack')
        else:
            recommendations['suitability_score'] = 0.5
            recommendations['messages'].append('Consider adding protein')

        recommendations['timing'] = 'Suitable for rest days or between workouts'

    else:  # general
        # Evaluate based on fitness goal
        if fitness_goal == 'muscle_building':
            if protein >= per_meal_protein * 0.8:
                recommendations['suitability_score'] = 0.8
                recommendations['messages'].append('Supports muscle building goals')
            else:
                recommendations['suitability_score'] = 0.5
                recommendations['messages'].append('Consider supplementing with more protein')

        elif fitness_goal == 'weight_loss':
            if protein >= 15 and sugar < 10 and fat < 10:
                recommendations['suitability_score'] = 0.9
                recommendations['messages'].append('Good for weight loss - high protein, low sugar')
            elif sugar > 20:
                recommendations['suitability_score'] = 0.4
                recommendations['messages'].append('High sugar content - not ideal for weight loss')
            else:
                recommendations['suitability_score'] = 0.6

    # Sugar warning
    if sugar > 15:
        recommendations['messages'].append(f'⚠ High sugar content ({sugar}g) - consume in moderation')

    return recommendations

def _analyze_for_fitness(nutrition_facts, fitness_goal, workout_timing):
    """Detailed fitness-focused analysis"""
    protein = nutrition_facts.get('protein', 0)
    carbs = nutrition_facts.get('carbohydrates', 0)
    fat = nutrition_facts.get('fat', 0)
    sugar = nutrition_facts.get('sugar', 0)
    calories = nutrition_facts.get('calories', 0)

    analysis = {
        'fitness_score': 0.0,
        'macro_breakdown': {},
        'strengths': [],
        'weaknesses': [],
        'best_use_case': ''
    }

    # Calculate macro percentages
    total_macros = (protein * 4) + (carbs * 4) + (fat * 9)
    if total_macros > 0:
        analysis['macro_breakdown'] = {
            'protein_percent': round((protein * 4 / total_macros) * 100),
            'carb_percent': round((carbs * 4 / total_macros) * 100),
            'fat_percent': round((fat * 9 / total_macros) * 100)
        }

    # Analyze for muscle building
    if fitness_goal == 'muscle_building':
        if protein >= 20:
            analysis['strengths'].append('High protein content excellent for muscle growth')
            analysis['fitness_score'] += 40

        if protein >= 10:
            analysis['fitness_score'] += 20

        if carbs >= 25:
            analysis['strengths'].append('Good carb content for energy')
            analysis['fitness_score'] += 20

        if sugar > 20:
            analysis['weaknesses'].append('High sugar - choose complex carbs instead')
            analysis['fitness_score'] -= 10

        if protein < 15:
            analysis['weaknesses'].append('Protein content could be higher for optimal muscle building')

    # Analyze for weight loss
    elif fitness_goal == 'weight_loss':
        if protein >= 15 and calories < 200:
            analysis['strengths'].append('High protein, low calorie - ideal for weight loss')
            analysis['fitness_score'] += 40

        if sugar < 5:
            analysis['strengths'].append('Low sugar content')
            analysis['fitness_score'] += 20

        if fat < 5:
            analysis['strengths'].append('Low fat')
            analysis['fitness_score'] += 20

        if sugar > 15:
            analysis['weaknesses'].append('High sugar - may hinder weight loss')
            analysis['fitness_score'] -= 20

        if calories > 300:
            analysis['weaknesses'].append('Relatively high calorie')
            analysis['fitness_score'] -= 10

    # Determine best use case
    if protein >= 20 and carbs >= 30:
        analysis['best_use_case'] = 'Post-workout recovery meal'
    elif protein >= 20 and sugar < 10:
        analysis['best_use_case'] = 'High-protein snack or muscle recovery'
    elif carbs >= 30 and fat < 5:
        analysis['best_use_case'] = 'Pre-workout energy source'
    elif protein >= 15:
        analysis['best_use_case'] = 'General protein supplementation'
    else:
        analysis['best_use_case'] = 'General snack - not optimized for fitness'

    analysis['fitness_score'] = max(0, min(100, analysis['fitness_score']))

    return analysis

def _determine_optimal_timing(nutrition_facts):
    """Determine optimal consumption timing based on macro profile"""
    protein = nutrition_facts.get('protein', 0)
    carbs = nutrition_facts.get('carbohydrates', 0)
    fat = nutrition_facts.get('fat', 0)
    sugar = nutrition_facts.get('sugar', 0)

    timing = {
        'optimal_time': '',
        'reasoning': '',
        'alternatives': []
    }

    # High protein, moderate carbs, low fat = Post-workout
    if protein >= 20 and carbs >= 20 and fat < 10:
        timing['optimal_time'] = 'Post-workout (within 45 minutes)'
        timing['reasoning'] = 'High protein and carbs support recovery without excess fat slowing digestion'

    # Moderate carbs, low fat = Pre-workout
    elif carbs >= 20 and fat < 5:
        timing['optimal_time'] = 'Pre-workout (30-60 minutes before)'
        timing['reasoning'] = 'Provides quick energy without fat that slows digestion'
        timing['alternatives'].append('Morning breakfast for energy')

    # High protein, low carbs/fat = Anytime protein
    elif protein >= 15 and carbs < 15 and fat < 10:
        timing['optimal_time'] = 'Anytime (especially between meals)'
        timing['reasoning'] = 'Lean protein source suitable for muscle maintenance throughout the day'
        timing['alternatives'].append('Before bed for overnight muscle recovery')

    # High carbs, moderate protein = Morning or pre-workout
    elif carbs >= 30:
        timing['optimal_time'] = 'Morning or pre-workout'
        timing['reasoning'] = 'High carb content provides sustained energy'

    else:
        timing['optimal_time'] = 'General consumption'
        timing['reasoning'] = 'Balanced macro profile suitable for regular meals'

    return timing
