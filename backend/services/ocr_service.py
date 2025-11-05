"""
OCR Service - Food Label Text Extraction
Implements layout-aware processing for Indian packaging
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
from typing import Dict, List, Tuple, Optional

class OCRService:
    """Advanced OCR service with layout-aware processing"""

    def __init__(self):
        """Initialize OCR service with custom configuration"""
        # Tesseract configuration for food labels
        self.tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,%-:/()'

    def process_food_label(self, image_path: str) -> Dict:
        """
        Main processing pipeline for food labels

        Args:
            image_path: Path to the food label image

        Returns:
            Dictionary containing extracted data and confidence scores
        """
        # Step 1: Load and preprocess image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")

        preprocessed = self._adaptive_preprocessing(image)

        # Step 2: Layout-aware segmentation
        segments = self._layout_analysis(preprocessed)

        # Step 3: Extract text from segments
        extracted_data = self._contextual_ocr(segments)

        # Step 4: Calculate confidence scores
        confidence = self._multi_dimensional_scoring(extracted_data, preprocessed)

        return {
            'nutrition_facts': extracted_data.get('nutrition_table', {}),
            'ingredients': extracted_data.get('ingredient_list', []),
            'symbols': extracted_data.get('symbols', {}),
            'confidence': confidence,
            'raw_text': extracted_data.get('raw_text', '')
        }

    def _adaptive_preprocessing(self, image: np.ndarray,
                                lighting_condition: str = "variable",
                                packaging_type: str = "indian") -> np.ndarray:
        """
        Adaptive preprocessing for Indian packaging

        Args:
            image: Input image array
            lighting_condition: Lighting conditions (low/normal/variable)
            packaging_type: Type of packaging

        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        # Adaptive thresholding for variable lighting
        binary = cv2.adaptiveThreshold(
            denoised, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        # Morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # Edge enhancement
        edges = cv2.Canny(cleaned, 50, 150)
        enhanced = cv2.addWeighted(cleaned, 0.8, edges, 0.2, 0)

        return enhanced

    def _layout_analysis(self, image: np.ndarray,
                        target_elements: List[str] = None) -> Dict[str, np.ndarray]:
        """
        Layout-aware segmentation to identify key elements

        Args:
            image: Preprocessed image
            target_elements: List of elements to detect

        Returns:
            Dictionary of segmented regions
        """
        if target_elements is None:
            target_elements = ["nutrition_table", "ingredient_list", "veg_nonveg_symbol"]

        segments = {}

        # Detect tables (nutrition facts)
        nutrition_table = self._detect_nutrition_table(image)
        if nutrition_table is not None:
            segments['nutrition_table'] = nutrition_table

        # Detect ingredient list area
        ingredient_area = self._detect_ingredient_area(image)
        if ingredient_area is not None:
            segments['ingredient_list'] = ingredient_area

        # Detect veg/non-veg symbols
        symbols = self._detect_symbols(image)
        if symbols:
            segments['symbols'] = symbols

        # Full image as fallback
        segments['full_image'] = image

        return segments

    def _detect_nutrition_table(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Detect nutrition table region using contour detection"""
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find rectangular contours that could be tables
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)

            # Nutrition tables are typically rectangular and of certain size
            if 0.5 < aspect_ratio < 2.0 and w > 100 and h > 100:
                return image[y:y+h, x:x+w]

        return None

    def _detect_ingredient_area(self, image: np.ndarray) -> Optional[np.ndarray]:
        """Detect ingredient list area"""
        # Ingredient lists typically have dense text
        # Use text density detection
        height, width = image.shape

        # Look in bottom half where ingredients are usually listed
        bottom_half = image[height//2:, :]

        return bottom_half

    def _detect_symbols(self, image: np.ndarray) -> Dict[str, bool]:
        """Detect veg/non-veg symbols using template matching or color detection"""
        symbols = {
            'vegetarian': False,
            'non_vegetarian': False
        }

        # Convert to color for green/brown dot detection
        # This is a simplified version - would use template matching in production
        # Look for circular shapes in specific color ranges

        return symbols

    def _contextual_ocr(self, segments: Dict[str, np.ndarray],
                       validation_rules: Dict = None) -> Dict:
        """
        Perform OCR with context-aware processing

        Args:
            segments: Segmented image regions
            validation_rules: FSSAI validation rules

        Returns:
            Extracted and validated data
        """
        extracted = {
            'raw_text': '',
            'nutrition_table': {},
            'ingredient_list': [],
            'symbols': {}
        }

        # Process full image first for raw text
        if 'full_image' in segments:
            pil_image = Image.fromarray(segments['full_image'])
            extracted['raw_text'] = pytesseract.image_to_string(pil_image, config=self.tesseract_config)

        # Process nutrition table
        if 'nutrition_table' in segments:
            nutrition_data = self._extract_nutrition_facts(segments['nutrition_table'])
            extracted['nutrition_table'] = nutrition_data

        # Process ingredient list
        if 'ingredient_list' in segments:
            ingredients = self._extract_ingredients(segments['ingredient_list'])
            extracted['ingredient_list'] = ingredients

        # Process symbols
        if 'symbols' in segments:
            extracted['symbols'] = segments['symbols']

        return extracted

    def _extract_nutrition_facts(self, table_image: np.ndarray) -> Dict[str, float]:
        """Extract nutrition facts from table region"""
        pil_image = Image.fromarray(table_image)
        text = pytesseract.image_to_string(pil_image, config=self.tesseract_config)

        nutrition_facts = {}

        # Common nutrition patterns
        patterns = {
            'protein': r'protein[:\s]+(\d+\.?\d*)\s*g',
            'carbohydrates': r'carbohydrate[s]?[:\s]+(\d+\.?\d*)\s*g',
            'fat': r'fat[:\s]+(\d+\.?\d*)\s*g',
            'calories': r'calories[:\s]+(\d+)',
            'sugar': r'sugar[s]?[:\s]+(\d+\.?\d*)\s*g',
            'sodium': r'sodium[:\s]+(\d+\.?\d*)\s*mg',
            'fiber': r'fiber[:\s]+(\d+\.?\d*)\s*g'
        }

        text_lower = text.lower()

        for nutrient, pattern in patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                try:
                    nutrition_facts[nutrient] = float(match.group(1))
                except ValueError:
                    pass

        return nutrition_facts

    def _extract_ingredients(self, ingredient_image: np.ndarray) -> List[str]:
        """Extract ingredient list"""
        pil_image = Image.fromarray(ingredient_image)
        text = pytesseract.image_to_string(pil_image, config=self.tesseract_config)

        # Look for ingredient list pattern
        ingredient_match = re.search(r'ingredients?[:\s]+(.+)', text.lower())

        if ingredient_match:
            ingredients_text = ingredient_match.group(1)
            # Split by commas and clean up
            ingredients = [ing.strip() for ing in ingredients_text.split(',')]
            return [ing for ing in ingredients if ing]

        return []

    def _multi_dimensional_scoring(self, extracted_data: Dict,
                                   preprocessed_image: np.ndarray,
                                   dimensions: List[str] = None) -> Dict[str, float]:
        """
        Multi-dimensional confidence scoring

        Args:
            extracted_data: Extracted text data
            preprocessed_image: Preprocessed image
            dimensions: Scoring dimensions

        Returns:
            Confidence scores for each dimension
        """
        if dimensions is None:
            dimensions = ["text_clarity", "regulatory_compliance", "nutrient_consistency"]

        scores = {}

        # Text clarity score based on image quality
        scores['text_clarity'] = self._calculate_text_clarity(preprocessed_image, extracted_data)

        # Regulatory compliance score (placeholder - would check FSSAI rules)
        scores['regulatory_compliance'] = self._calculate_compliance_score(extracted_data)

        # Nutrient consistency score
        scores['nutrient_consistency'] = self._calculate_consistency_score(extracted_data)

        # Overall confidence
        scores['overall'] = sum(scores.values()) / len(scores)

        return scores

    def _calculate_text_clarity(self, image: np.ndarray, extracted_data: Dict) -> float:
        """Calculate text clarity score based on image quality and OCR confidence"""
        # Check image sharpness using Laplacian variance
        laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()

        # Normalize to 0-1 range (typical values: 10-1000)
        clarity_score = min(laplacian_var / 500, 1.0)

        # Check if we extracted meaningful data
        if extracted_data.get('nutrition_table'):
            clarity_score *= 1.1  # Boost if nutrition data found

        return min(clarity_score, 1.0)

    def _calculate_compliance_score(self, extracted_data: Dict) -> float:
        """Calculate regulatory compliance confidence"""
        score = 0.5  # Base score

        nutrition = extracted_data.get('nutrition_table', {})

        # Check for required fields
        required_fields = ['protein', 'carbohydrates', 'fat', 'calories']
        found_fields = sum(1 for field in required_fields if field in nutrition)

        score += (found_fields / len(required_fields)) * 0.5

        return min(score, 1.0)

    def _calculate_consistency_score(self, extracted_data: Dict) -> float:
        """Calculate nutrient consistency score"""
        nutrition = extracted_data.get('nutrition_table', {})

        if not nutrition:
            return 0.0

        # Check if values are reasonable
        score = 1.0

        # Protein shouldn't exceed 100g per serving
        if nutrition.get('protein', 0) > 100:
            score -= 0.3

        # Total nutrients shouldn't be wildly inconsistent
        total = nutrition.get('protein', 0) + nutrition.get('carbohydrates', 0) + nutrition.get('fat', 0)
        if total > 150:  # Per serving values should be reasonable
            score -= 0.2

        return max(score, 0.0)

def validated_results(extracted_data: Dict, confidence: Dict) -> Dict:
    """Validate and format final results"""
    return {
        'success': confidence['overall'] > 0.5,
        'data': extracted_data,
        'confidence': confidence,
        'recommendation': 'high' if confidence['overall'] > 0.8 else 'medium' if confidence['overall'] > 0.5 else 'low'
    }
