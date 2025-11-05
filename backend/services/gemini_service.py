"""
Google Gemini AI Service
Uses Gemini 2.0 Flash for nutrition extraction and report generation
Enhanced with detailed prompts for comprehensive insights
"""

import google.generativeai as genai
import os
from PIL import Image
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    """Service for Google Gemini AI integration"""

    def __init__(self):
        """Initialize Gemini with API key"""
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)

        # Use Gemini 2.0 Flash model
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Generation config for detailed outputs
        self.generation_config = {
            "temperature": 0.7,  # Balanced creativity and consistency
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 4096,  # Increased for detailed reports
        }

    def extract_nutrition_from_image(self, image_path: str) -> Dict:
        """Extract nutrition facts from food label image using Gemini Vision"""
        try:
            image = Image.open(image_path)
            prompt = """Analyze this food label image and extract ALL nutrition information.

Return ONLY a valid JSON object with this exact structure (use null for missing values):

{
  "product_name": "string or null",
  "brand": "string or null",
  "serving_size": "string or null",
  "servings_per_container": "number or null",
  "nutrition_facts": {
    "calories": number or null,
    "protein": number or null,
    "carbohydrates": number or null,
    "total_carbs": number or null,
    "dietary_fiber": number or null,
    "sugar": number or null,
    "total_fat": number or null,
    "saturated_fat": number or null,
    "trans_fat": number or null,
    "cholesterol": number or null,
    "sodium": number or null,
    "vitamins": {}
  },
  "ingredients": ["list of ingredients"],
  "allergens": ["list of allergens if mentioned"],
  "claims": ["high protein", "low sugar", etc.],
  "vegetarian": true/false/null,
  "vegan": true/false/null,
  "expiry_date": "string or null",
  "batch_number": "string or null"
}

IMPORTANT:
- Extract numeric values only (remove units like 'g', 'mg')
- All nutrition values should be per serving
- Be accurate with the numbers you see
- If something is not visible, use null"""

            response = self.model.generate_content(
                [prompt, image],
                generation_config=self.generation_config
            )

            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()

            nutrition_data = json.loads(result_text)
            return {
                'success': True,
                'data': nutrition_data,
                'confidence': 'high',
                'source': 'gemini-2.0-flash'
            }

        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Failed to parse JSON: {str(e)}',
                'raw_response': response.text if 'response' in locals() else None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error extracting nutrition: {str(e)}'
            }

    def generate_comprehensive_report(
        self,
        nutrition_data: Dict,
        fssai_verification: Dict,
        user_profile: Optional[Dict] = None
    ) -> Dict:
        """Generate a comprehensive nutrition report using Gemini"""
        try:
            # Extract metadata fields
            serving_size = nutrition_data.get('serving_size', 'Not specified')
            net_weight = nutrition_data.get('net_weight', 'Not specified')
            servings_per_container = nutrition_data.get('servings_per_container', 'Not specified')
            ingredients = nutrition_data.get('ingredients', [])

            prompt = f"""You are an expert nutritionist, FSSAI compliance specialist, and fitness coach. Generate a detailed, professional nutrition analysis report.

PRODUCT INFORMATION:
- Serving Size: {serving_size}
- Net Weight/Quantity: {net_weight}
- Servings Per Container: {servings_per_container}
- Ingredients: {', '.join(ingredients) if ingredients else 'Not provided'}

NUTRITION DATA (per serving):
{json.dumps(nutrition_data, indent=2)}

FSSAI VERIFICATION STATUS:
{json.dumps(fssai_verification, indent=2)}

IMPORTANT: Use the serving size, net weight, and servings per container information to provide accurate calculations:
- Calculate total product nutrition (serving data × servings per container)
- Calculate per 100g values if possible
- Provide context on portion sizes
- Compare serving size to typical portion sizes
"""
            if user_profile:
                prompt += f"""
USER PROFILE:
- Fitness Goal: {user_profile.get('fitness_goal', 'Not specified')}
- Weight: {user_profile.get('weight', 'Not specified')} kg
- Height: {user_profile.get('height', 'Not specified')} cm
- Age: {user_profile.get('age', 'Not specified')}
"""

            prompt += f"""
Generate a comprehensive, well-structured report with rich insights and actionable advice:

## 📊 PRODUCT OVERVIEW
Provide 3-4 key highlights about this product's nutritional profile and what makes it unique.

### Packaging & Portion Information
- **Serving Size**: {serving_size}
- **Net Weight**: {net_weight}
- **Servings Per Container**: {servings_per_container}
- **Total Product Nutrition**: Calculate and show total nutrients in entire package
- **Per 100g Analysis**: Normalize nutrition values to per 100g for easy comparison
- **Portion Context**: Is this serving size realistic? Compare to typical consumption patterns

## 🔬 DETAILED NUTRITION ANALYSIS

### Protein Analysis
- Amount per serving and percentage of daily needs
- Quality assessment (complete/incomplete protein)
- Suitability for muscle building (compare to 20-30g benchmark)
- Timing recommendations for consumption

### Carbohydrates Breakdown
- Total carbs and type (simple vs complex)
- Fiber content and digestive health benefits
- Glycemic impact and blood sugar considerations
- Energy provision analysis

### Fats Profile
- Total fat breakdown (saturated, unsaturated, trans)
- Heart health implications
- Essential fatty acids presence
- Omega-3/6 balance if known

### Micronutrients & Other
- Sodium level and cardiovascular impact (compare to 2300mg daily limit)
- Sugar content and metabolic effects (compare to 25g daily WHO limit)
- Vitamins and minerals if present
- Additives, preservatives, and their safety

## ⚖️ FSSAI COMPLIANCE ANALYSIS
- **Overall Status**: [Compliant/Non-Compliant] - detailed explanation
- **Specific Claims Verification**: Analyze each nutritional claim against exact FSSAI thresholds
- **Labeling Quality**: Assessment of information transparency
- **Consumer Protection**: Any misleading marketing concerns or false claims

## 💪 FITNESS & HEALTH SUITABILITY

### For Muscle Building (Bodybuilders, Athletes)
- Protein adequacy score: X/10
- Post-workout suitability: [Excellent/Good/Average/Poor]
- BCAAs and leucine content estimation
- Carb-to-protein ratio analysis
- **Rating**: ⭐⭐⭐⭐⭐ (X/5 stars)

### For Weight Loss (Calorie Deficit)
- Caloric density analysis
- Satiety factor (protein + fiber content)
- Thermic effect of food
- Glycemic load impact
- **Rating**: ⭐⭐⭐⭐⭐ (X/5 stars)

### For General Health & Wellness
- Nutrient density score
- Processing level (whole food vs ultra-processed)
- Long-term consumption safety
- Disease prevention potential
- **Rating**: ⭐⭐⭐⭐⭐ (X/5 stars)

### For Specific Conditions
- Diabetes management suitability
- Heart health (low sodium/saturated fat)
- Digestive health (fiber content)

## ⚠️ HEALTH CONCERNS & RED FLAGS
List any:
- Excessive sodium, sugar, or trans fats
- Harmful additives or preservatives
- Allergen risks
- Ultra-processed food markers
- Long-term health risks

## ✅ POSITIVE NUTRITIONAL HIGHLIGHTS
List beneficial aspects:
- High-quality nutrients present
- Beneficial ingredients
- Clean label features
- Unique health benefits

## 🎯 PERSONALIZED RECOMMENDATIONS

### Ideal For:
- Specific demographics who would benefit most
- Fitness goals this product supports
- Lifestyle patterns that match

### Not Recommended For:
- Medical conditions to avoid
- Fitness goals it doesn't support
- Dietary restrictions it violates

### Smart Consumption Guide:
- **Best Timing**: When to consume for maximum benefit
- **Optimal Frequency**: How often per week/day
- **Portion Control**: Recommended serving adjustments
- **Food Pairing**: What to combine it with for balanced nutrition

## 📊 NUTRITIONAL COMPARISON

| Metric | This Product | Indian RDA | WHO Guideline | Verdict |
|--------|-------------|-----------|---------------|---------|
| Protein | {nutrition_data.get('protein', 0)}g | 50g (avg) | 0.8g/kg | [Good/Average/Low] |
| Sugar | {nutrition_data.get('sugar', 0)}g | <25g | <25g | [Good/Average/High] |
| Sodium | {nutrition_data.get('sodium', 0)}mg | <2300mg | <2000mg | [Good/Average/High] |
| Fiber | {nutrition_data.get('fiber', 0)}g | 25g | 25-30g | [Good/Average/Low] |
| Saturated Fat | {nutrition_data.get('saturated_fat', 0)}g | <20g | <10% calories | [Good/Average/High] |

## 🏆 OVERALL ASSESSMENT

**Nutrition Score**: XX/100
(Breakdown: Protein-20, Carbs-20, Fats-20, Micronutrients-20, Processing-20)

**Health Score**: ⭐⭐⭐⭐⭐ (X/5 stars)
**Value for Money**: ⭐⭐⭐⭐⭐ (X/5 stars)
**Taste vs Nutrition Balance**: ⭐⭐⭐⭐⭐ (X/5 stars)

### Final Verdict:
[2-3 sentences with clear BUY/CONSIDER/AVOID recommendation and reasoning]

### Better Alternatives (if score < 75):
If this product scores below 75, suggest 2-3 specific alternative products or ingredients that would better meet nutritional goals.

## 💡 PRO TIPS
- Meal prep ideas using this product
- Recipe suggestions for balanced nutrition
- Shopping advice for similar products

---
*Analysis based on: FSSAI Food Safety Standards 2024, WHO Nutrition Guidelines, Indian Council of Medical Research (ICMR) Dietary Guidelines, and evidence-based nutrition science*

BE SPECIFIC WITH NUMBERS. USE REAL THRESHOLDS. GIVE ACTIONABLE ADVICE. COMPARE TO STANDARDS. BE HONEST ABOUT PROS AND CONS."""

            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            return {
                'success': True,
                'report': response.text,
                'generated_by': 'gemini-2.0-flash'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating report: {str(e)}'
            }

    def analyze_ingredients_safety(self, ingredients: List[str]) -> Dict:
        """Analyze ingredient safety with detailed breakdown"""
        try:
            prompt = f"""As a food safety expert, analyze these ingredients comprehensively:

INGREDIENTS LIST:
{json.dumps(ingredients, indent=2)}

Provide a detailed safety analysis:

## 🔍 INGREDIENT-BY-INGREDIENT ANALYSIS

For EACH ingredient, provide:
- **Name**: [Ingredient name]
- **Purpose**: Why it's added (flavor, preservation, texture, etc.)
- **Safety Level**: ✅ Safe / ⚠️ Caution / ❌ Concerning
- **Health Impact**: Brief explanation

## ✅ SAFE & BENEFICIAL INGREDIENTS
List ingredients that are:
- Natural, whole-food based
- Nutritionally valuable
- Generally recognized as safe (GRAS)
- No known health concerns

## ⚠️ INGREDIENTS OF CONCERN
Identify any:
- Artificial preservatives (BHA, BHT, etc.)
- Artificial colors (Tartrazine, etc.)
- High fructose corn syrup
- Hydrogenated oils (trans fats)
- MSG and flavor enhancers
- Explain WHY each is concerning

## 🚫 ALLERGEN WARNINGS
Identify allergens from these categories:
- Milk/Dairy products
- Eggs
- Peanuts & Tree nuts
- Soy
- Wheat/Gluten
- Fish & Shellfish
- Sesame

## 📊 PROCESSING LEVEL ASSESSMENT
Classify as:
- **Minimally Processed** (whole foods, minimal alteration)
- **Processed** (added salt, sugar, oil)
- **Ultra-Processed** (industrial formulations, cosmetic additives)

**Level**: [Classification]
**Explanation**: Why this classification

## 🏥 HEALTH IMPLICATIONS

### Short-term Effects:
- Immediate impacts on energy, digestion, etc.

### Long-term Considerations:
- Chronic health effects of regular consumption
- Disease risk factors
- Metabolic impacts

## 🌍 REGULATORY STATUS
- FSSAI approval status
- WHO/FAO food safety standards compliance
- Any banned substances in other countries

## 📈 OVERALL SAFETY SCORE

**Safety Score**: XX/100

Breakdown:
- Natural ingredients: [Points]
- Absence of harmful additives: [Points]
- Allergen safety: [Points]
- Processing level: [Points]
- Nutritional value: [Points]

## 💡 CONSUMER ADVICE
- Who should DEFINITELY avoid this product
- Who can consume it safely
- Frequency recommendations
- Red flags to watch for

## 🔄 HEALTHIER ALTERNATIVES
If score < 70, suggest what ingredients to look for instead.

BE SPECIFIC. CITE ACTUAL RESEARCH OR REGULATIONS WHEN RELEVANT. BE BALANCED BUT HONEST."""

            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            return {
                'success': True,
                'analysis': response.text,
                'generated_by': 'gemini-2.0-flash'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error analyzing ingredients: {str(e)}'
            }

    def generate_personalized_recommendation(
        self,
        nutrition_data: Dict,
        user_profile: Dict,
        workout_timing: str = 'general'
    ) -> Dict:
        """Generate highly personalized recommendation"""
        try:
            prompt = f"""As a certified nutritionist and fitness coach, provide a detailed personalized recommendation.

PRODUCT NUTRITION:
{json.dumps(nutrition_data, indent=2)}

USER PROFILE:
- Fitness Goal: {user_profile.get('fitness_goal', 'maintenance')}
- Weight: {user_profile.get('weight', 70)} kg
- Height: {user_profile.get('height', 170)} cm
- Age: {user_profile.get('age', 25)}
- Gender: {user_profile.get('gender', 'male')}

CONSUMPTION TIMING: {workout_timing}

Generate a comprehensive personalized analysis:

## 🎯 SUITABILITY SCORE FOR THIS USER

**Overall Score**: XX/100

Breakdown:
- Goal alignment: XX/30
- Nutritional adequacy: XX/25
- Timing appropriateness: XX/20
- Health compatibility: XX/15
- Value proposition: XX/10

## ✅ KEY BENEFITS FOR YOU

1. **[Specific Benefit]**
   - Why it matters for your {user_profile.get('fitness_goal')} goal
   - Quantified impact (e.g., "Provides 40% of your daily protein needs")

2. **[Specific Benefit]**
   - Relevant to your profile
   - Actionable outcome

3. **[Specific Benefit]**
   - Personalized advantage

## ⚠️ POTENTIAL CONCERNS

1. **[Concern if any]**
   - Why it matters specifically for you
   - How to mitigate

2. **[Concern if any]**
   - Specific to your goal/profile

## ⏰ OPTIMAL CONSUMPTION STRATEGY

### Best Timing:
- **Primary**: [Exact time and why]
- **Alternative**: [Backup timing option]
- **Avoid**: [When not to consume]

### Portion Guidance:
- Recommended serving for your goals
- Adjustments based on activity level
- Frequency per week

### Food Pairing:
- What to eat it with for maximum benefit
- Complementary nutrients to add
- Combinations to avoid

## 🏋️ WORKOUT INTEGRATION

For {workout_timing} consumption:
- How it supports your workout
- Nutrient timing benefits
- Recovery/performance impact
- Specific recommendations

## 📊 GOAL PROGRESS IMPACT

For your {user_profile.get('fitness_goal')} goal:
- How this fits your macros
- Contribution to daily targets
- Frequency recommendation
- Progress timeline impact

## 💡 PRO TIPS PERSONALIZED FOR YOU

1. [Specific actionable tip]
2. [Specific actionable tip]
3. [Specific actionable tip]

## 🔄 IF THIS ISN'T IDEAL (Score <70)

**Better Options To Look For:**
- [Specific alternative product type]
- [Specific nutritional profile to seek]
- [Specific brands or categories]

**What to Prioritize:**
- [Specific nutrient targets]
- [Specific ingredient preferences]

## 🎯 BOTTOM LINE

[2-3 sentences with clear HIGHLY RECOMMEND / GOOD OPTION / CONSIDER ALTERNATIVES / AVOID verdict specific to this user's profile and goals]

BE HONEST. BE SPECIFIC TO THIS USER. USE THEIR ACTUAL DATA. GIVE NUMBERS. BE PRACTICAL."""

            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            return {
                'success': True,
                'recommendation': response.text,
                'generated_by': 'gemini-2.0-flash'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating recommendation: {str(e)}'
            }

    def compare_products_ai(self, products: List[Dict]) -> Dict:
        """Compare products with detailed analysis"""
        try:
            prompt = f"""As a nutrition expert, provide a comprehensive product comparison:

PRODUCTS TO COMPARE:
{json.dumps(products, indent=2)}

## 📊 HEAD-TO-HEAD COMPARISON

### Nutrition Comparison Table:

| Metric | Product 1 | Product 2 | Product 3 | Best Choice |
|--------|-----------|-----------|-----------|-------------|
| Protein (g) | X | Y | Z | [Winner] |
| Carbs (g) | X | Y | Z | [Winner] |
| Fats (g) | X | Y | Z | [Winner] |
| Calories | X | Y | Z | [Winner] |
| Fiber (g) | X | Y | Z | [Winner] |
| Sugar (g) | X | Y | Z | [Winner] |
| Sodium (mg) | X | Y | Z | [Winner] |
| Price/Serving | X | Y | Z | [Winner] |

## 🏆 WINNERS BY CATEGORY

### Best for Muscle Building
**Winner**: [Product Name]
**Why**: [Specific reasons with numbers]
**Score**: XX/100

### Best for Weight Loss
**Winner**: [Product Name]
**Why**: [Specific reasons]
**Score**: XX/100

### Best for General Health
**Winner**: [Product Name]
**Why**: [Specific reasons]
**Score**: XX/100

### Best Value for Money
**Winner**: [Product Name]
**Why**: [Cost-benefit analysis]

### Healthiest Overall
**Winner**: [Product Name]
**Why**: [Comprehensive health assessment]

## 📈 DETAILED PRODUCT RANKINGS

1. **[Product Name]** - Overall Score: XX/100
   - Strengths: [List 3]
   - Weaknesses: [List 2]
   - Best for: [User type]

2. **[Product Name]** - Overall Score: XX/100
   - Strengths: [List 3]
   - Weaknesses: [List 2]
   - Best for: [User type]

3. **[Product Name]** - Overall Score: XX/100
   - Strengths: [List 3]
   - Weaknesses: [List 2]
   - Best for: [User type]

## 🎯 FINAL RECOMMENDATION

**Your Best Choice**: [Product Name]

**Reasoning**: [3-4 sentences explaining why this is the best option overall, considering nutrition, health, and value]

**When to Choose Alternatives**:
- Choose [Product 2] if [specific scenario]
- Choose [Product 3] if [specific scenario]

## 💰 VALUE ANALYSIS
- Cost per gram of protein
- Cost per 100 calories
- Overall value verdict

BE SPECIFIC. USE ACTUAL NUMBERS. BE PRACTICAL. GIVE CLEAR WINNER."""

            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            return {
                'success': True,
                'comparison': response.text,
                'generated_by': 'gemini-2.0-flash'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error comparing products: {str(e)}'
            }

    def answer_nutrition_question(self, question: str, context: Dict = None) -> Dict:
        """Answer nutrition questions with detailed explanations"""
        try:
            prompt = f"""As a nutrition expert and FSSAI specialist, provide a comprehensive answer:

QUESTION: {question}
"""
            if context:
                prompt += f"""
CONTEXT:
{json.dumps(context, indent=2)}
"""

            prompt += """
Provide a detailed, well-structured answer with:

## 📚 DIRECT ANSWER
[Clear, concise answer to the question]

## 🔬 DETAILED EXPLANATION
[In-depth explanation with science and evidence]

## 📋 FSSAI/WHO GUIDELINES
[Relevant regulatory standards and recommendations]

## 💡 PRACTICAL APPLICATION
[How to apply this knowledge in real life]

## ⚠️ IMPORTANT CONSIDERATIONS
[Any caveats, exceptions, or warnings]

## 🔗 REFERENCES
[Mention relevant FSSAI regulations, WHO guidelines, or scientific principles]

BE ACCURATE. CITE STANDARDS. BE PRACTICAL. USE INDIAN CONTEXT."""

            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            return {
                'success': True,
                'answer': response.text,
                'generated_by': 'gemini-2.0-flash'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error answering question: {str(e)}'
            }

    def generate_meal_suggestions(
        self,
        scanned_products: List[Dict],
        user_profile: Dict,
        meal_type: str = 'any'
    ) -> Dict:
        """Generate meal suggestions based on products"""
        try:
            prompt = f"""As a nutrition coach, create practical meal suggestions:

AVAILABLE PRODUCTS:
{json.dumps(scanned_products, indent=2)}

USER PROFILE:
- Goal: {user_profile.get('fitness_goal', 'maintenance')}
- Daily Protein Target: {user_profile.get('targets', {}).get('daily_protein', 140)}g
- Daily Calorie Target: {user_profile.get('targets', {}).get('daily_calories', 2400)} kcal

MEAL TYPE: {meal_type}

Create 3 practical meal ideas using these products, considering Indian eating habits and preferences.

BE PRACTICAL AND DELICIOUS. CONSIDER INDIAN TASTES."""

            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            return {
                'success': True,
                'suggestions': response.text,
                'generated_by': 'gemini-2.0-flash'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating meal suggestions: {str(e)}'
            }

    def generate_healthier_alternatives(
        self,
        nutrition_data: Dict,
        fssai_verification: Dict,
        user_profile: Optional[Dict] = None
    ) -> Dict:
        """Generate healthier alternative product suggestions"""
        try:
            product_name = nutrition_data.get('product_name', 'this product')
            brand = nutrition_data.get('brand', 'Unknown')
            category = nutrition_data.get('category', 'food product')

            prompt = f"""As a nutrition expert and food industry specialist, suggest healthier alternative products.

CURRENT PRODUCT:
- Name: {product_name}
- Brand: {brand}
- Category: {category}

NUTRITION DATA (per serving):
{json.dumps(nutrition_data.get('nutrition_facts', {}), indent=2)}

FSSAI COMPLIANCE:
{json.dumps(fssai_verification, indent=2)}

INGREDIENTS:
{', '.join(nutrition_data.get('ingredients', []))}
"""

            if user_profile:
                prompt += f"""
USER PROFILE:
- Fitness Goal: {user_profile.get('fitness_goal', 'general health')}
- Dietary Preferences: {user_profile.get('dietary_preference', 'none specified')}
- Age: {user_profile.get('age', 'not specified')}
"""

            prompt += """
Generate a comprehensive alternatives recommendation with:

## 🎯 WHY LOOK FOR ALTERNATIVES?

**Current Product Issues** (if any):
- List specific nutritional concerns (high sugar, low protein, excessive sodium, etc.)
- Processing level concerns
- Ingredient red flags
- FSSAI compliance issues
- Better value available

**Overall Assessment**: [Is this product okay or should user definitely switch?]

## 🏆 TOP 3 HEALTHIER ALTERNATIVES

For each alternative, provide:

### Alternative #1: [Specific Brand & Product Name]
**Brand**: [Real brand name that exists in India]
**Why It's Better**:
- Higher protein by X grams
- Lower sugar by X grams
- Better ingredient quality
- [Specific improvements]

**Nutrition Comparison**:
| Metric | Original | Alternative | Difference |
|--------|----------|-------------|------------|
| Calories | X | Y | Better/Worse |
| Protein | X | Y | +Xg |
| Sugar | X | Y | -Xg |
| Sodium | X | Y | -Xmg |
| Fiber | X | Y | +Xg |

**Where to Buy**: [Availability in India - online/stores]
**Price Range**: ₹XX - ₹XX
**Best For**: [Specific user type or goal]
**Rating**: ⭐⭐⭐⭐⭐ (X/5)

---

### Alternative #2: [Specific Brand & Product Name]
[Same format as Alternative #1]

---

### Alternative #3: [Specific Brand & Product Name]
[Same format as Alternative #1]

---

## 🥗 WHOLE FOOD ALTERNATIVES

If the current product is processed, suggest whole food options:

**Instead of [Product]**, try:
1. **[Whole Food Option 1]**
   - Nutrition benefits
   - How to prepare/consume
   - Cost comparison

2. **[Whole Food Option 2]**
   - Why it's better
   - Practical usage

3. **[Whole Food Option 3]**
   - Nutritional advantages
   - Easy recipes

## 🔄 HOMEMADE VERSION

**DIY Recipe**: Make your own healthier version at home

**Ingredients You'll Need**:
- [List simple ingredients]

**Quick Recipe** (5-10 minutes):
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Nutrition Advantage**: [Compare to original]
**Cost Savings**: Save ₹XX per serving
**Shelf Life**: [How long it lasts]

## 💰 BUDGET-FRIENDLY ALTERNATIVES

If money is a concern:

1. **[Affordable Option 1]** (₹XX)
   - Still healthier than original
   - Where to find

2. **[Affordable Option 2]** (₹XX)
   - Good nutrition at lower cost

## 🎯 CATEGORY-SPECIFIC RECOMMENDATIONS

**For Muscle Building**: Choose [Specific product] because [reason]
**For Weight Loss**: Choose [Specific product] because [reason]
**For General Health**: Choose [Specific product] because [reason]
**For Diabetes**: Choose [Specific product] because [reason]
**For Heart Health**: Choose [Specific product] because [reason]

## 🛒 SHOPPING TIPS

**What to Look For on Labels**:
- Protein content: At least Xg per serving
- Sugar content: Under Xg per serving
- Sodium: Under Xmg per serving
- Fiber: At least Xg per serving
- First 3 ingredients should be: [List]
- Avoid: [Ingredients to avoid]

**Brands Known for Quality** (in this category):
1. [Brand 1] - Known for [quality aspect]
2. [Brand 2] - Known for [quality aspect]
3. [Brand 3] - Known for [quality aspect]

## ⚡ QUICK DECISION GUIDE

**Stick with current product if**: [Specific conditions]
**Switch to Alternative #1 if**: [Your priority is X]
**Switch to Alternative #2 if**: [Your priority is Y]
**Go homemade if**: [You have time and want best nutrition]

## 📊 UPGRADE PATH

**Good → Better → Best**:
- **Good**: [Current product with modifications]
- **Better**: [Alternative #1 or #2]
- **Best**: [Alternative #3 or homemade version]

---

IMPORTANT INSTRUCTIONS:
- Suggest REAL brands and products available in India
- Be specific with product names (not just "choose any protein bar")
- Provide actual nutritional comparisons with numbers
- Consider Indian market availability
- Include both premium and budget options
- Be honest - if current product is fine, say so
- Prioritize based on user's goals
- Make recommendations actionable and practical"""

            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            return {
                'success': True,
                'alternatives': response.text,
                'generated_by': 'gemini-2.0-flash'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error generating alternatives: {str(e)}'
            }
