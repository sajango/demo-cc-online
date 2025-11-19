# Food Analysis API Documentation

## Overview

API tích hợp với Z-AI SDK cho phép người dùng upload ảnh món ăn và nhận được phân tích chi tiết về món ăn đó, bao gồm tên món, thành phần và ước tính calo.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Không yêu cầu authentication cho endpoint này (có thể thêm sau nếu cần).

## Endpoints

### 1. Analyze Food Image

Phân tích ảnh món ăn và trả về thông tin chi tiết.

**Endpoint:** `POST /food-analysis/analyze`

**Request:**

- Method: `POST`
- Content-Type: `multipart/form-data`
- Body Parameters:
  - `file` (required): Image file (JPEG, PNG, WEBP)
    - Max size: 10MB
    - Supported formats: image/jpeg, image/jpg, image/png, image/webp

**Example Request (cURL):**

```bash
curl -X POST "http://localhost:8000/api/v1/food-analysis/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/food-image.jpg"
```

**Example Request (Python):**

```python
import requests

url = "http://localhost:8000/api/v1/food-analysis/analyze"
files = {"file": open("food-image.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

**Example Request (JavaScript/Fetch):**

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/food-analysis/analyze', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

**Response (Success - 200 OK):**

```json
{
  "dish_name": "Phở Bò",
  "ingredients": [
    "Bánh phở",
    "Thịt bò",
    "Hành lá",
    "Ngò gai",
    "Giá đỗ",
    "Nước dùng"
  ],
  "estimated_calories": "350-450 kcal",
  "analysis_details": "Đây là món phở bò truyền thống Việt Nam..."
}
```

**Response (Cannot Identify - 200 OK):**

```json
{
  "dish_name": "tôi không rõ",
  "ingredients": null,
  "estimated_calories": null,
  "analysis_details": "Không thể xác định món ăn từ hình ảnh này..."
}
```

**Response (Error - 400 Bad Request):**

```json
{
  "detail": "Invalid file type. Allowed types: image/jpeg, image/jpg, image/png, image/webp"
}
```

**Response (Error - 500 Internal Server Error):**

```json
{
  "detail": "Failed to analyze image: [error message]"
}
```

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `dish_name` | string | Tên món ăn hoặc "tôi không rõ" nếu không xác định được |
| `ingredients` | array[string] \| null | Danh sách thành phần món ăn (có thể là null nếu không xác định được) |
| `estimated_calories` | string \| null | Ước tính khối lượng calo (ví dụ: "350-450 kcal") |
| `analysis_details` | string \| null | Thông tin chi tiết về phân tích từ AI |

### 2. Health Check

Kiểm tra trạng thái của Food Analysis service.

**Endpoint:** `GET /food-analysis/health`

**Request:**

- Method: `GET`
- No parameters required

**Example Request:**

```bash
curl -X GET "http://localhost:8000/api/v1/food-analysis/health"
```

**Response (200 OK):**

```json
{
  "status": "healthy",
  "api_key_configured": true,
  "message": "Food analysis service is running"
}
```

## Configuration

### Environment Variables

Cần cấu hình các biến môi trường sau trong file `.env`:

```bash
# Z-AI Integration
ZAI_API_KEY=your-zai-api-key-here
```

### Lấy Z-AI API Key

1. Truy cập [Z.ai Open Platform](https://z.ai) (cho người dùng quốc tế)
2. Hoặc [Zhipu AI](https://open.bigmodel.cn) (cho người dùng Trung Quốc)
3. Đăng ký tài khoản và tạo API key
4. Copy API key vào file `.env`

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Phân tích thành công |
| 400 | Bad Request - File không hợp lệ hoặc quá lớn |
| 500 | Internal Server Error - Lỗi server hoặc Z-AI API |

## Limitations

- File size tối đa: 10MB
- Supported image formats: JPEG, JPG, PNG, WEBP
- Rate limit: Phụ thuộc vào Z-AI API plan của bạn

## Example Use Cases

### 1. Upload và phân tích ảnh món ăn

```python
import requests

def analyze_food(image_path: str) -> dict:
    url = "http://localhost:8000/api/v1/food-analysis/analyze"

    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.json()}")

# Sử dụng
result = analyze_food("pho_bo.jpg")
print(f"Món ăn: {result['dish_name']}")
print(f"Thành phần: {result['ingredients']}")
print(f"Calo: {result['estimated_calories']}")
```

### 2. Web form với HTML/JavaScript

```html
<!DOCTYPE html>
<html>
<head>
    <title>Food Analysis</title>
</head>
<body>
    <h1>Phân tích món ăn</h1>
    <input type="file" id="fileInput" accept="image/*">
    <button onclick="analyzeFood()">Phân tích</button>
    <div id="result"></div>

    <script>
        async function analyzeFood() {
            const fileInput = document.getElementById('fileInput');
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            try {
                const response = await fetch('http://localhost:8000/api/v1/food-analysis/analyze', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                document.getElementById('result').innerHTML = `
                    <h2>${data.dish_name}</h2>
                    <p><strong>Thành phần:</strong> ${data.ingredients?.join(', ') || 'N/A'}</p>
                    <p><strong>Calo:</strong> ${data.estimated_calories || 'N/A'}</p>
                `;
            } catch (error) {
                console.error('Error:', error);
                alert('Có lỗi xảy ra khi phân tích ảnh');
            }
        }
    </script>
</body>
</html>
```

## Testing

### Using FastAPI Swagger UI

1. Chạy server: `uvicorn src.main:app --reload`
2. Truy cập: `http://localhost:8000/docs`
3. Tìm endpoint `/api/v1/food-analysis/analyze`
4. Click "Try it out"
5. Upload ảnh và click "Execute"

### Using pytest

```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_analyze_food_image():
    with open("test_food.jpg", "rb") as f:
        response = client.post(
            "/api/v1/food-analysis/analyze",
            files={"file": ("test_food.jpg", f, "image/jpeg")}
        )

    assert response.status_code == 200
    data = response.json()
    assert "dish_name" in data
    assert "ingredients" in data
    assert "estimated_calories" in data
```

## Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra configuration (ZAI_API_KEY)
2. Kiểm tra format và kích thước ảnh
3. Xem logs của server
4. Liên hệ support team

## Version History

- **v1.0.0** (2025-11-19): Initial release
  - Analyze food images with Z-AI SDK
  - Return dish name, ingredients, and calorie estimation
  - Support JPEG, PNG, WEBP formats
