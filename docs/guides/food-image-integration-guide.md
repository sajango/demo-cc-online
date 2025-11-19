# Food Image Integration Guide (Tiếng Việt & English)

## Tổng quan / Overview

**Vietnamese:** Hướng dẫn tích hợp API upload và phân tích hình ảnh món ăn sử dụng Z-AI SDK.

**English:** Guide for integrating food image upload and analysis API using Z-AI SDK.

---

## Cài đặt / Installation

### 1. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

**Packages mới được thêm:**
- `Pillow==10.1.0` - Xử lý hình ảnh / Image processing
- `zai-sdk==0.0.4.2` - Z-AI Python SDK

### 2. Cấu hình Environment Variables

Sao chép `.env.example` sang `.env` và cập nhật:

```env
# Z-AI Configuration (Bắt buộc / Required)
ZAI_API_KEY=your-zai-api-key-here
ZAI_BASE_URL=https://api.z.ai/api/paas/v4/
```

**Lấy Z-AI API Key:**
1. Truy cập https://z.ai
2. Đăng ký / Đăng nhập
3. Vào phần API Keys
4. Tạo API key mới
5. Copy key vào file `.env`

---

## Kiến trúc / Architecture

### Clean Architecture Layers

```
┌─────────────────────────────────────────────┐
│  Presentation Layer (API Endpoints)        │
│  src/presentation/api/v1/food_images.py    │
│  - POST /api/v1/food-images/upload         │
│  - POST /api/v1/food-images/upload/stream  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Application Layer (Use Cases)              │
│  src/application/use_cases/                 │
│  - UploadFoodImageUseCase                   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Infrastructure Layer (Services)            │
│  src/infrastructure/services/               │
│  - ImageProcessorService (Pillow)           │
│  - ZaiService (Z-AI SDK)                    │
└─────────────────────────────────────────────┘
```

### Luồng xử lý / Processing Flow

**Vietnamese:**
1. **Upload** → API nhận file hình ảnh từ client
2. **Validation** → Kiểm tra định dạng, kích thước file
3. **Conversion** → Chuyển đổi sang JPG/PNG
4. **Z-AI Analysis** → Gửi ảnh tới Z-AI để phân tích
5. **Response** → Trả về kết quả phân tích

**English:**
1. **Upload** → API receives image file from client
2. **Validation** → Check format and file size
3. **Conversion** → Convert to JPG/PNG
4. **Z-AI Analysis** → Send image to Z-AI for analysis
5. **Response** → Return analysis results

---

## API Endpoints

### 1. Upload cơ bản / Standard Upload

**Endpoint:** `POST /api/v1/food-images/upload`

**Không cần xác thực / No authentication required**

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/food-images/upload" \
  -F "file=@food-image.jpg" \
  -F "target_format=JPEG"
```

**Response:**
```json
{
  "success": true,
  "message": "Image uploaded and analyzed successfully",
  "image_info": {
    "original_filename": "food-image.jpg",
    "converted_format": "JPEG",
    "width": 1920,
    "height": 1080
  },
  "analysis": "Phân tích món ăn từ Z-AI..."
}
```

### 2. Upload với Streaming

**Endpoint:** `POST /api/v1/food-images/upload/stream`

**Streaming response** cho phân tích real-time.

---

## Code Examples

### Python Client

```python
import requests

# Upload food image
url = "http://localhost:8000/api/v1/food-images/upload"
files = {"file": open("banh_mi.jpg", "rb")}
data = {"target_format": "JPEG"}

response = requests.post(url, files=files, data=data)
result = response.json()

if result["success"]:
    print(f"Phân tích: {result['analysis']}")
    print(f"Kích thước: {result['image_info']['width']}x{result['image_info']['height']}")
else:
    print(f"Lỗi: {result['message']}")
```

### JavaScript (React/Vue)

```javascript
async function uploadFoodImage(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('target_format', 'JPEG');

  try {
    const response = await fetch('http://localhost:8000/api/v1/food-images/upload', {
      method: 'POST',
      body: formData
    });

    const result = await response.json();

    if (result.success) {
      console.log('Phân tích:', result.analysis);
      console.log('Thông tin ảnh:', result.image_info);
    } else {
      console.error('Lỗi:', result.message);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}
```

### Streaming Example (JavaScript)

```javascript
async function uploadFoodImageStreaming(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://localhost:8000/api/v1/food-images/upload/stream', {
    method: 'POST',
    body: formData
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));

        if (data.type === 'image_info') {
          console.log('Thông tin ảnh:', data.data);
        } else if (data.type === 'analysis_chunk') {
          // Hiển thị từng phần phân tích real-time
          console.log('Chunk:', data.data);
        } else if (data.type === 'complete') {
          console.log('Hoàn tất phân tích');
        }
      }
    }
  }
}
```

---

## Testing

### 1. Unit Tests

```bash
# Chạy test cho image processor
pytest tests/unit/test_image_processor.py -v

# Chạy tất cả unit tests
pytest tests/unit/ -v
```

### 2. Manual Testing với Swagger UI

1. Khởi động server:
```bash
uvicorn src.main:app --reload
```

2. Mở Swagger UI: http://localhost:8000/docs

3. Tìm section "Food Images"

4. Click "Try it out" → Chọn file ảnh → "Execute"

### 3. Testing với cURL

```bash
# Test với ảnh JPEG
curl -X POST "http://localhost:8000/api/v1/food-images/upload" \
  -F "file=@test-food.jpg"

# Test với ảnh PNG, convert sang JPEG
curl -X POST "http://localhost:8000/api/v1/food-images/upload" \
  -F "file=@test-food.png" \
  -F "target_format=JPEG"
```

---

## Xử lý lỗi / Error Handling

### Các lỗi thường gặp / Common Errors

| Mã lỗi / Code | Nguyên nhân / Cause | Giải pháp / Solution |
|---------------|---------------------|----------------------|
| 400 | File không phải hình ảnh / Invalid image | Kiểm tra định dạng file |
| 400 | File quá lớn (>10MB) / File too large | Nén ảnh trước khi upload |
| 400 | Định dạng không hỗ trợ / Unsupported format | Dùng JPEG, PNG, GIF, BMP, WebP |
| 500 | Lỗi kết nối Z-AI / Z-AI connection error | Kiểm tra API key và mạng |

### Error Handling Code

```python
try:
    result = await upload_food_image(file)
    if result["success"]:
        # Xử lý thành công
        process_analysis(result["analysis"])
    else:
        # Xử lý lỗi từ API
        show_error(result["message"])
except requests.exceptions.RequestException as e:
    # Lỗi network
    show_error("Lỗi kết nối mạng")
except Exception as e:
    # Lỗi không xác định
    show_error(f"Lỗi: {str(e)}")
```

---

## Best Practices

### 1. Tối ưu hóa ảnh / Image Optimization

**Vietnamese:**
- Nén ảnh trước khi upload (500KB - 2MB là tối ưu)
- Sử dụng độ phân giải phù hợp (1024x768 hoặc cao hơn)
- Đảm bảo ánh sáng tốt và món ăn rõ ràng

**English:**
- Compress images before upload (500KB - 2MB optimal)
- Use appropriate resolution (1024x768 or higher)
- Ensure good lighting and clear food visibility

### 2. Xử lý Response

```python
# Kiểm tra success trước khi xử lý
if result.get("success"):
    analysis = result.get("analysis", "")
    image_info = result.get("image_info", {})

    # Lưu token usage để tracking
    usage = result.get("zai_metadata", {}).get("usage", {})
    total_tokens = usage.get("total_tokens", 0)

    # Xử lý analysis
    display_food_analysis(analysis, image_info)
```

### 3. Performance Optimization

```python
# Sử dụng streaming cho UX tốt hơn
async def upload_with_progress(file):
    # Hiển thị progress bar
    show_progress("Đang upload...")

    # Sử dụng streaming endpoint
    async for chunk in stream_upload(file):
        update_progress(chunk)

    show_progress("Hoàn tất!")
```

---

## Security Considerations

### 1. Rate Limiting

**Vietnamese:** Nên implement rate limiting trong production để tránh abuse.

**English:** Implement rate limiting in production to prevent abuse.

```python
# Ví dụ với FastAPI rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/upload")
@limiter.limit("10/minute")  # Giới hạn 10 requests/phút
async def upload_food_image(request: Request, file: UploadFile):
    # ...
```

### 2. File Validation

**Vietnamese:** API tự động validate:
- Kích thước file (max 10MB)
- Định dạng file (JPEG, PNG, GIF, BMP, WebP)
- Nội dung file (verify bằng PIL)

**English:** API automatically validates:
- File size (max 10MB)
- File format (JPEG, PNG, GIF, BMP, WebP)
- File content (verified by PIL)

### 3. API Key Security

**Vietnamese:**
- Không lưu API key trong code
- Sử dụng environment variables
- Rotate key định kỳ

**English:**
- Never store API keys in code
- Use environment variables
- Rotate keys regularly

---

## Troubleshooting

### Lỗi Z-AI Connection

```
Failed to analyze image with Z-AI: Connection timeout
```

**Giải pháp / Solutions:**
1. Kiểm tra `ZAI_API_KEY` trong `.env`
2. Verify API key còn hoạt động trên Z.AI platform
3. Kiểm tra network connection
4. Xem Z-AI service status

### Lỗi Image Validation

```
Image validation failed: File size exceeds maximum allowed size
```

**Giải pháp / Solutions:**
1. Nén ảnh trước khi upload
2. Giảm độ phân giải nếu cần
3. Sử dụng công cụ nén ảnh online

### Import Errors

```
ModuleNotFoundError: No module named 'zai'
```

**Giải pháp / Solutions:**
```bash
# Cài đặt lại dependencies
pip install -r requirements.txt

# Hoặc cài đặt riêng
pip install zai-sdk==0.0.4.2 Pillow==10.1.0
```

---

## Development Workflow

### 1. Local Development

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env với Z-AI API key

# Run server
uvicorn src.main:app --reload
```

### 2. Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_image_processor.py

# Run with coverage
pytest --cov=src tests/
```

### 3. Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

---

## Support & Resources

- **Z-AI Documentation:** https://docs.z.ai
- **Z-AI GitHub:** https://github.com/zai-org/z-ai-sdk-python
- **Pillow Documentation:** https://pillow.readthedocs.io
- **FastAPI Documentation:** https://fastapi.tiangolo.com

---

## Changelog

### Version 1.0.0 (2025-11-19)

**Added:**
- Food image upload API endpoint (no authentication)
- Image validation and format conversion (JPEG/PNG)
- Z-AI integration for food analysis
- Streaming upload endpoint for real-time analysis
- Comprehensive error handling
- Unit tests for image processing
- API documentation

**Dependencies:**
- zai-sdk 0.0.4.2
- Pillow 10.1.0
