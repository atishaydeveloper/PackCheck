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
        # Multiple Tesseract configurations for different scenarios
        self.configs = {
            'default': r'--oem 3 --psm 6',  # Assume uniform text block
            'sparse': r'--oem 3 --psm 11',  # Sparse text without order
            'single_block': r'--oem 3 --psm 6',  # Single uniform block
            'single_line': r'--oem 3 --psm 7',  # Single text line
            'auto': r'--oem 3 --psm 3',  # Fully automatic page segmentation
        }

    def process_food_label(self, image_path: str) -> Dict:
        """
        Main processing pipeline for food labels with multiple OCR passes

        Args:
            image_path: Path to the food label image

        Returns:
            Dictionary containing extracted data and confidence scores
        """
        # Step 1: Load original image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")

        # Step 2: Try multiple preprocessing methods and combine results
        # OPTIMIZED: Use only best-performing combinations (8 passes instead of 20)
        all_text = []
        preprocessed_images = []

        # Method 1: Adaptive preprocessing (original) - works well for most labels
        preprocessed1 = self._adaptive_preprocessing(image)
        preprocessed_images.append(('adaptive', preprocessed1, ['default', 'sparse']))

        # Method 2: High contrast preprocessing - for faded/low contrast labels
        preprocessed2 = self._high_contrast_preprocessing(image)
        preprocessed_images.append(('high_contrast', preprocessed2, ['default', 'auto']))

        # Method 3: Brightness normalization - for uneven lighting
        preprocessed3 = self._brightness_normalization(image)
        preprocessed_images.append(('brightness', preprocessed3, ['default']))

        # Method 4: Scale up small text - for tiny text
        preprocessed4 = self._scale_preprocessing(image)
        preprocessed_images.append(('scaled', preprocessed4, ['default', 'single_block', 'sparse']))

        # Step 3: Extract text using optimized config combinations (8 passes total)
        for method_name, prep_image, config_names in preprocessed_images:
            for config_name in config_names:
                try:
                    pil_image = Image.fromarray(prep_image)
                    config = self.configs[config_name]
                    text = pytesseract.image_to_string(pil_image, config=config)
                    if text and len(text.strip()) > 10:  # Ignore very short outputs
                        all_text.append(text)
                        print(f"✓ OCR pass: {method_name}/{config_name} - {len(text)} chars")
                except Exception as e:
                    print(f"✗ OCR pass failed ({method_name}, {config_name}): {e}")
                    continue

        # Step 4: Combine and deduplicate extracted text
        combined_text = '\n'.join(all_text)

        # Step 5: Layout-aware segmentation on best preprocessed image
        segments = self._layout_analysis(preprocessed1)
        segments['full_image'] = preprocessed1

        # Step 6: Extract structured data
        extracted_data = self._contextual_ocr(segments, combined_text)

        # Step 7: Calculate confidence scores
        confidence = self._multi_dimensional_scoring(extracted_data, preprocessed1)

        return {
            'nutrition_facts': extracted_data.get('nutrition_table', {}),
            'ingredients': extracted_data.get('ingredient_list', []),
            'symbols': extracted_data.get('symbols', {}),
            'serving_size': extracted_data.get('serving_size'),
            'net_weight': extracted_data.get('net_weight'),
            'servings_per_container': extracted_data.get('servings_per_container'),
            'confidence': confidence,
            'raw_text': combined_text
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

    def _high_contrast_preprocessing(self, image: np.ndarray) -> np.ndarray:
        """
        High contrast preprocessing for better text extraction
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Strong binary thresholding
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return binary

    def _brightness_normalization(self, image: np.ndarray) -> np.ndarray:
        """
        Normalize brightness for consistent text extraction
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)

        # Merge channels
        lab = cv2.merge([l, a, b])

        # Convert back to BGR then to grayscale
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)

        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        return denoised

    def _scale_preprocessing(self, image: np.ndarray, scale_factor: float = 2.0) -> np.ndarray:
        """
        Scale up image to help with small text
        """
        # Scale up the image
        height, width = image.shape[:2]
        scaled = cv2.resize(image, (int(width * scale_factor), int(height * scale_factor)),
                           interpolation=cv2.INTER_CUBIC)

        # Convert to grayscale
        gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)

        # Sharpen
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        sharpened = cv2.filter2D(gray, -1, kernel)

        # Binary threshold
        _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return binary

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
                       combined_text: str = None,
                       validation_rules: Dict = None) -> Dict:
        """
        Perform OCR with context-aware processing

        Args:
            segments: Segmented image regions
            combined_text: Pre-extracted text from multiple OCR passes
            validation_rules: FSSAI validation rules

        Returns:
            Extracted and validated data
        """
        extracted = {
            'raw_text': combined_text or '',
            'nutrition_table': {},
            'ingredient_list': [],
            'symbols': {},
            'serving_size': None,
            'net_weight': None,
            'servings_per_container': None
        }

        # Use combined text if available, otherwise extract from full image
        if not combined_text and 'full_image' in segments:
            pil_image = Image.fromarray(segments['full_image'])
            extracted['raw_text'] = pytesseract.image_to_string(pil_image, config=self.configs['default'])

        # Extract serving size, net weight, and servings from raw text
        if extracted['raw_text']:
            extracted['serving_size'] = self._extract_serving_size(extracted['raw_text'])
            extracted['net_weight'] = self._extract_net_weight(extracted['raw_text'])
            extracted['servings_per_container'] = self._extract_servings_per_container(extracted['raw_text'])

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
        """Extract nutrition facts from table region using optimized OCR passes"""
        nutrition_facts = {}

        # Try only best configs for tables (3 passes instead of 5)
        all_text = []
        pil_image = Image.fromarray(table_image)

        best_configs = ['default', 'single_block', 'auto']  # Best for tables

        for config_name in best_configs:
            try:
                config = self.configs[config_name]
                text = pytesseract.image_to_string(pil_image, config=config)
                if text:
                    all_text.append(text)
            except:
                continue

        # Combine all extracted text
        combined_text = '\n'.join(all_text)

        # Enhanced nutrition patterns (more flexible)
        patterns = {
            'protein': [
                r'protein[:\s]+(\d+\.?\d*)\s*g',
                r'protein[:\s]*(\d+\.?\d*)',
                r'prot[a-z]*[:\s]+(\d+\.?\d*)'
            ],
            'carbohydrates': [
                r'carbohydrate[s]?[:\s]+(\d+\.?\d*)\s*g',
                r'carb[s]?[:\s]+(\d+\.?\d*)',
                r'total\s+carb[s]?[:\s]+(\d+\.?\d*)'
            ],
            'fat': [
                r'total\s+fat[:\s]+(\d+\.?\d*)\s*g',
                r'fat[:\s]+(\d+\.?\d*)\s*g',
                r'fat[:\s]*(\d+\.?\d*)'
            ],
            'calories': [
                r'calories[:\s]+(\d+)',
                r'energy[:\s]+(\d+)\s*kcal',
                r'energy[:\s]+(\d+)'
            ],
            'sugar': [
                r'sugar[s]?[:\s]+(\d+\.?\d*)\s*g',
                r'sugar[s]?[:\s]*(\d+\.?\d*)',
                r'total\s+sugar[s]?[:\s]+(\d+\.?\d*)'
            ],
            'sodium': [
                r'sodium[:\s]+(\d+\.?\d*)\s*mg',
                r'sodium[:\s]*(\d+\.?\d*)',
                r'salt[:\s]+(\d+\.?\d*)'
            ],
            'fiber': [
                r'fiber[:\s]+(\d+\.?\d*)\s*g',
                r'dietary\s+fiber[:\s]+(\d+\.?\d*)',
                r'fibre[:\s]+(\d+\.?\d*)'
            ],
            'saturated_fat': [
                r'saturated\s+fat[:\s]+(\d+\.?\d*)\s*g',
                r'saturated[:\s]+(\d+\.?\d*)'
            ],
            'trans_fat': [
                r'trans\s+fat[:\s]+(\d+\.?\d*)\s*g',
                r'trans[:\s]+(\d+\.?\d*)'
            ]
        }

        text_lower = combined_text.lower()

        for nutrient, pattern_list in patterns.items():
            if nutrient in nutrition_facts:
                continue  # Already found
            for pattern in pattern_list:
                match = re.search(pattern, text_lower)
                if match:
                    try:
                        value = float(match.group(1))
                        # Sanity check: nutrition values shouldn't be too large
                        if value < 1000:
                            nutrition_facts[nutrient] = value
                            break
                    except (ValueError, IndexError):
                        continue

        return nutrition_facts

    def _extract_serving_size(self, text: str) -> Optional[str]:
        """
        Extract serving size from text

        Examples: "30g", "1 cup (240ml)", "2 pieces", "100g", "1 scoop (30g)"
        """
        text_lower = text.lower()

        # Patterns for serving size
        patterns = [
            r'serving\s+size[:\s]+([0-9]+\.?[0-9]*\s*(?:g|mg|kg|ml|l|cup|cups|piece|pieces|scoop|scoops|tablespoon|tbsp|teaspoon|tsp)(?:\s*\([^)]+\))?)',
            r'serv\.?\s+size[:\s]+([0-9]+\.?[0-9]*\s*(?:g|mg|kg|ml|l|cup|cups|piece|pieces|scoop|scoops|tablespoon|tbsp|teaspoon|tsp)(?:\s*\([^)]+\))?)',
            r'per\s+serving[:\s]+([0-9]+\.?[0-9]*\s*(?:g|mg|kg|ml|l|cup|cups|piece|pieces|scoop|scoops))',
            r'(?:^|\n)serving[:\s]+([0-9]+\.?[0-9]*\s*(?:g|mg|kg|ml|l|cup|cups|piece|pieces|scoop|scoops))',
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip()

        return None

    def _extract_net_weight(self, text: str) -> Optional[str]:
        """
        Extract net weight/quantity from text

        Examples: "500g", "1kg", "250ml", "1L", "24 pieces", "Net Wt: 500g"
        """
        text_lower = text.lower()

        # Patterns for net weight
        patterns = [
            r'net\s+(?:weight|wt|quantity|qty|contents?)[:\s]+([0-9]+\.?[0-9]*\s*(?:g|mg|kg|ml|l|pieces?))',
            r'net\s+(?:wt|qty)[.:\s]+([0-9]+\.?[0-9]*\s*(?:g|mg|kg|ml|l|pieces?))',
            r'(?:weight|quantity)[:\s]+([0-9]+\.?[0-9]*\s*(?:g|mg|kg|ml|l|pieces?))',
            r'contents?[:\s]+([0-9]+\.?[0-9]*\s*(?:g|mg|kg|ml|l|pieces?))',
            # Match standalone weight at beginning or after newline
            r'(?:^|\n)([0-9]+\.?[0-9]*\s*(?:kg|g|l|ml))\s*(?:\n|$)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip()

        return None

    def _extract_servings_per_container(self, text: str) -> Optional[float]:
        """
        Extract servings per container from text

        Examples: "Servings: 10", "Servings per container: 20", "Contains 5 servings"
        """
        text_lower = text.lower()

        # Patterns for servings per container
        patterns = [
            r'servings?\s+per\s+(?:container|package|pack)[:\s]+([0-9]+\.?[0-9]*)',
            r'servings?\s+per\s+(?:container|package|pack)[:\s]+(?:about|approx\.?|approximately)?\s*([0-9]+\.?[0-9]*)',
            r'(?:contains|has)\s+([0-9]+\.?[0-9]*)\s+servings?',
            r'(?:^|\n)servings?[:\s]+([0-9]+\.?[0-9]*)',
            r'no\.?\s+of\s+servings?[:\s]+([0-9]+\.?[0-9]*)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    pass

        return None

    def _extract_ingredients(self, ingredient_image: np.ndarray) -> List[str]:
        """Extract ingredient list using optimized OCR passes"""
        all_text = []
        pil_image = Image.fromarray(ingredient_image)

        # Try only best configs for ingredient lists (2 passes)
        best_configs = ['default', 'sparse']  # Best for dense text lists

        for config_name in best_configs:
            try:
                config = self.configs[config_name]
                text = pytesseract.image_to_string(pil_image, config=config)
                if text:
                    all_text.append(text)
            except:
                continue

        # Combine all extracted text
        combined_text = '\n'.join(all_text)

        # Look for ingredient list pattern
        ingredient_match = re.search(r'ingredients?[:\s]+(.+)', combined_text.lower())

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
