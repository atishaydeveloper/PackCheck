# PackCheck API Documentation

Base URL: `http://localhost:5000/api`

## Authentication

Currently, the API does not require authentication for development. Production deployment should implement JWT-based authentication.

## Endpoints

### Scan Endpoints

#### POST /api/scan/
Scan and process a food label image.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `image`: Image file (required)
  - `claims[]`: Array of claims made on packaging (optional)

**Response:**
```json
{
  "success": true,
  "ocr_results": {
    "nutrition_facts": {
      "protein": 15.0,
      "carbohydrates": 30.0,
      "fat": 5.0,
      "calories": 250
    },
    "ingredients": ["wheat", "milk", "sugar"],
    "confidence": {
      "overall": 0.85,
      "text_clarity": 0.9,
      "regulatory_compliance": 0.8
    }
  },
  "fssai_verification": {
    "overall_compliance": true,
    "trust_score": 0.9,
    "verifications": { ... }
  },
  "allergen_info": {
    "allergens_detected": ["wheat", "milk"],
    "warning": true
  }
}
```

#### POST /api/scan/batch
Scan multiple labels at once.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `images[]`: Multiple image files

**Response:**
```json
{
  "success": true,
  "total": 3,
  "processed": 3,
  "results": [ ... ]
}
```

#### POST /api/scan/validate
Validate manually entered nutrition data.

**Request:**
```json
{
  "nutrition_facts": {
    "protein": 20.0,
    "carbohydrates": 40.0,
    "fat": 10.0
  },
  "claims": ["high protein"]
}
```

**Response:**
```json
{
  "success": true,
  "verification": { ... }
}
```

### Nutrition Endpoints

#### GET /api/nutrition/:product_id
Get nutrition information for a product.

**Response:**
```json
{
  "success": true,
  "product_id": "prod123",
  "data": {
    "nutrition_facts": { ... },
    "metadata": { ... }
  }
}
```

#### POST /api/nutrition/store
Store nutrition data for a product.

**Request:**
```json
{
  "product_id": "prod123",
  "nutrition_facts": { ... },
  "metadata": {
    "name": "Protein Bar",
    "brand": "FitSnack"
  }
}
```

#### GET /api/nutrition/search
Search for products.

**Query Parameters:**
- `query`: Search query
- `min_protein`: Minimum protein content
- `max_sugar`: Maximum sugar content

**Response:**
```json
{
  "success": true,
  "count": 5,
  "results": [ ... ]
}
```

#### POST /api/nutrition/compare
Compare multiple products.

**Request:**
```json
{
  "product_ids": ["prod1", "prod2", "prod3"]
}
```

**Response:**
```json
{
  "success": true,
  "products": [ ... ],
  "analysis": {
    "highest_protein": { ... },
    "lowest_sugar": { ... },
    "best_for_fitness": { ... }
  }
}
```

### Verification Endpoints

#### POST /api/verify/fssai
Verify FSSAI compliance.

**Request:**
```json
{
  "nutrition_facts": {
    "protein": 15.0,
    "sugar": 5.0
  },
  "claims": ["high protein", "low sugar"]
}
```

**Response:**
```json
{
  "success": true,
  "verification": {
    "overall_compliance": true,
    "trust_score": 0.95,
    "verifications": {
      "protein": {
        "compliant": true,
        "message": "Product meets FSSAI 'High Protein' standard"
      }
    }
  }
}
```

#### POST /api/verify/protein
Verify protein claim specifically.

**Request:**
```json
{
  "protein_content": 15.0,
  "serving_size": 100.0,
  "claim": "high protein"
}
```

#### POST /api/verify/expiry
Verify expiry date.

**Request:**
```json
{
  "expiry_date": "31/12/2025"
}
```

#### POST /api/verify/allergens
Detect allergens in ingredients.

**Request:**
```json
{
  "ingredients": ["wheat flour", "milk powder", "peanuts"]
}
```

#### GET /api/verify/standards
Get FSSAI and WHO standards.

### Personalization Endpoints

#### POST /api/personalize/profile
Create or update user profile.

**Request:**
```json
{
  "user_id": "user123",
  "fitness_goal": "muscle_building",
  "body_metrics": {
    "weight": 70,
    "height": 175,
    "age": 25,
    "gender": "male"
  }
}
```

#### GET /api/personalize/profile/:user_id
Get user profile.

#### POST /api/personalize/recommend
Get personalized recommendations.

**Request:**
```json
{
  "user_id": "user123",
  "nutrition_facts": {
    "protein": 20.0,
    "carbohydrates": 30.0
  },
  "workout_timing": "post_workout"
}
```

**Response:**
```json
{
  "success": true,
  "recommendations": {
    "suitability_score": 0.9,
    "messages": ["Perfect post-workout recovery food"],
    "timing": "Consume within 30-45 minutes post-workout"
  }
}
```

#### POST /api/personalize/analyze
Analyze product for fitness goals.

**Request:**
```json
{
  "nutrition_facts": { ... },
  "fitness_goal": "muscle_building",
  "workout_timing": "post_workout"
}
```

### Community Endpoints

#### POST /api/community/verify
Submit community verification.

**Request:**
```json
{
  "product_id": "prod123",
  "user_id": "user456",
  "verification_type": "confirm",
  "data": { ... },
  "confidence": "high"
}
```

#### GET /api/community/verify/:product_id
Get community verifications for a product.

#### GET /api/community/corrections
Get pending corrections.

**Query Parameters:**
- `status`: pending, approved, rejected

#### POST /api/community/corrections/:verification_id/approve
Approve a community correction (dietitian action).

#### POST /api/community/corrections/:verification_id/reject
Reject a community correction (dietitian action).

#### GET /api/community/leaderboard
Get community contributors leaderboard.

#### GET /api/community/badge
Check if product has community verified badge.

**Query Parameters:**
- `product_id`: Product ID

## Error Responses

All endpoints return errors in the following format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

HTTP Status Codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

Currently no rate limiting is implemented. Production deployment should implement appropriate rate limiting.

## Examples

### cURL Examples

**Scan a label:**
```bash
curl -X POST http://localhost:5000/api/scan/ \
  -F "image=@label.jpg" \
  -F "claims=high protein"
```

**Get FSSAI verification:**
```bash
curl -X POST http://localhost:5000/api/verify/fssai \
  -H "Content-Type: application/json" \
  -d '{
    "nutrition_facts": {"protein": 15, "sugar": 5},
    "claims": ["high protein"]
  }'
```

### JavaScript/Axios Examples

**Scan a label:**
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

const response = await axios.post('/api/scan/', formData);
console.log(response.data);
```

**Get personalized recommendations:**
```javascript
const response = await axios.post('/api/personalize/recommend', {
  user_id: 'user123',
  nutrition_facts: {
    protein: 20,
    carbohydrates: 30
  },
  workout_timing: 'post_workout'
});
console.log(response.data.recommendations);
```
