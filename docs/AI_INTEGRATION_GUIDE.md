# AI Integration Guide for PackCheck

## Current Status: NO AI Integrated ❌

PackCheck currently uses:
- **Tesseract OCR**: Rule-based text extraction
- **Pattern Matching**: Regex for nutrition facts
- **Conditional Logic**: FSSAI verification rules

**NO machine learning or AI models are currently used.**

---

## Option 1: OpenAI GPT-4 Vision (Easiest) ⭐

### Cost: ~$0.01 per image

### Implementation:

```python
# backend/services/ai_ocr_service.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_nutrition_with_gpt4(image_path):
    """Extract nutrition facts using GPT-4 Vision"""

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Extract nutrition facts from this food label image.
                        Return ONLY a JSON object with this structure:
                        {
                            "protein": <grams>,
                            "carbohydrates": <grams>,
                            "fat": <grams>,
                            "sugar": <grams>,
                            "sodium": <mg>,
                            "calories": <kcal>,
                            "serving_size": "<size>",
                            "ingredients": ["ingredient1", "ingredient2"],
                            "claims": ["high protein", "low sugar"]
                        }
                        If any value is not found, use null."""
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_data}"
                    }
                ]
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content
```

### Setup:
1. Get API key from https://platform.openai.com/
2. Add to `.env`: `OPENAI_API_KEY=sk-...`
3. Install: `pip install openai`
4. Update `api/scan.py` to use this service

---

## Option 2: Google Cloud Vision API

### Cost: Free tier (1000 images/month), then ~$1.50 per 1000

```python
from google.cloud import vision

def extract_with_google_vision(image_path):
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    texts = response.text_annotations
    return texts[0].description if texts else ""
```

### Setup:
1. Create project at https://console.cloud.google.com/
2. Enable Vision API
3. Download credentials JSON
4. `pip install google-cloud-vision`

---

## Option 3: Train Custom ML Model (Most Complex)

### Steps:

1. **Collect Dataset**
   - 1000+ labeled food label images
   - Annotate nutrition tables, ingredients

2. **Choose Architecture**
   - **Object Detection**: YOLOv8 to find nutrition table
   - **OCR**: TrOCR or EasyOCR for text extraction
   - **NER**: BERT for entity recognition

3. **Training**
   ```bash
   # Example with YOLOv8
   pip install ultralytics

   from ultralytics import YOLO

   model = YOLO('yolov8n.pt')
   model.train(data='nutrition_labels.yaml', epochs=100)
   ```

4. **Deploy Model**
   ```python
   from ultralytics import YOLO

   model = YOLO('best.pt')
   results = model.predict('label_image.jpg')
   ```

---

## Option 4: Hugging Face Transformers

### Use pre-trained models:

```python
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-printed')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-printed')

def extract_text_with_trocr(image_path):
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return text
```

### Setup:
```bash
pip install transformers torch pillow
```

---

## Option 5: Claude AI API (Anthropic)

```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def extract_with_claude(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64.b64encode(image_data).decode()
                        }
                    },
                    {
                        "type": "text",
                        "text": "Extract nutrition facts from this food label as JSON"
                    }
                ]
            }
        ]
    )

    return message.content
```

---

## Recommended Approach for PackCheck

### Phase 1: Quick Win (1 week)
Use **GPT-4 Vision API**:
- Fastest to implement
- Best accuracy
- Cost: ~$0.01 per scan
- Good for MVP/testing

### Phase 2: Cost Optimization (1 month)
Hybrid approach:
- Try Tesseract first (free)
- If confidence < 70%, use GPT-4
- Reduces API costs by 60-80%

### Phase 3: Full ML (3-6 months)
Train custom model:
- Collect 5000+ Indian food labels
- Fine-tune YOLOv8 + TrOCR
- Host on your own servers
- Zero per-scan cost

---

## Implementation Example: Adding GPT-4 Vision

### Step 1: Install Package
```bash
pip install openai pillow
```

### Step 2: Update requirements.txt
```
openai==1.3.0
```

### Step 3: Add to .env
```
OPENAI_API_KEY=sk-proj-your-key-here
USE_AI_OCR=true
```

### Step 4: Create AI Service
Create `backend/services/ai_ocr_service.py` (see code above)

### Step 5: Update scan.py
```python
from services.ai_ocr_service import extract_nutrition_with_gpt4

# In scan_label() function:
if os.getenv('USE_AI_OCR') == 'true':
    ai_result = extract_nutrition_with_gpt4(filepath)
    nutrition_data = json.loads(ai_result)
else:
    ocr_result = ocr_service.process_food_label(filepath)
    nutrition_data = ocr_result.get('nutrition_facts', {})
```

---

## Comparison Table

| Solution | Cost | Accuracy | Speed | Complexity |
|----------|------|----------|-------|------------|
| Current (Tesseract) | Free | 60-70% | Fast | Low |
| GPT-4 Vision | $0.01/scan | 95%+ | 2-3s | Low |
| Google Vision | $0.0015/scan | 85-90% | 1-2s | Medium |
| Custom ML | $0/scan* | 90%+ | <1s | High |
| Hugging Face | Free | 75-85% | 2-4s | Medium |

*After initial training cost

---

## Cost Estimates

### For 10,000 scans/month:

- **Tesseract**: $0 (but lower accuracy)
- **GPT-4 Vision**: $100/month
- **Google Vision**: $15/month
- **Custom Model**: $50/month (hosting) + $2000 (one-time training)
- **Hugging Face**: $20/month (hosting)

---

## Quick Start: Add GPT-4 Now

1. Get OpenAI key: https://platform.openai.com/api-keys
2. Add to `.env`: `OPENAI_API_KEY=sk-...`
3. Create the AI service file (see Option 1)
4. Update scan.py imports
5. Test!

---

## Testing AI Integration

```bash
# Test GPT-4 Vision
curl -X POST http://localhost:5000/api/scan/ \
  -F "image=@test_label.jpg" \
  -F "use_ai=true"
```

---

## Which Should You Choose?

### For Your Project (PackCheck):

**Recommendation: Start with GPT-4 Vision**

Why:
- ✅ Quick to implement (1 day)
- ✅ Highest accuracy for Indian labels
- ✅ Understands context (claims, allergens)
- ✅ No training data needed
- ✅ Works immediately
- ✅ Can extract ingredients naturally

**Cost**: $100/month for 10k scans is acceptable for MVP

**Later**: Switch to custom model once you have:
- 5000+ labeled images
- Proven product-market fit
- Budget for ML engineer

---

## Next Steps

1. **Decide which AI to use**
2. **Get API keys** (if using cloud AI)
3. **Follow implementation guide above**
4. **Test with real food labels**
5. **Compare accuracy**: Tesseract vs AI
6. **Monitor costs**

---

Would you like me to implement GPT-4 Vision integration for you?
