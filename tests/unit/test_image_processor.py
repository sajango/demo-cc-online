"""Unit tests for ImageProcessorService."""
import io
import pytest
from PIL import Image

from src.infrastructure.services.image_processor import ImageProcessorService


@pytest.fixture
def image_processor():
    """Fixture for ImageProcessorService."""
    return ImageProcessorService()


@pytest.fixture
def valid_jpeg_bytes():
    """Fixture for valid JPEG image bytes."""
    img = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.read()


@pytest.fixture
def valid_png_bytes():
    """Fixture for valid PNG image bytes."""
    img = Image.new("RGBA", (100, 100), color=(0, 128, 255, 200))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()


def test_validate_image_success_jpeg(image_processor, valid_jpeg_bytes):
    """Test successful validation of JPEG image."""
    is_valid, error = image_processor.validate_image(valid_jpeg_bytes, "test.jpg")
    assert is_valid is True
    assert error == ""


def test_validate_image_success_png(image_processor, valid_png_bytes):
    """Test successful validation of PNG image."""
    is_valid, error = image_processor.validate_image(valid_png_bytes, "test.png")
    assert is_valid is True
    assert error == ""


def test_validate_image_invalid_extension(image_processor, valid_jpeg_bytes):
    """Test validation fails for invalid extension."""
    is_valid, error = image_processor.validate_image(valid_jpeg_bytes, "test.txt")
    assert is_valid is False
    assert "not allowed" in error


def test_validate_image_invalid_content(image_processor):
    """Test validation fails for invalid image content."""
    invalid_content = b"This is not an image"
    is_valid, error = image_processor.validate_image(invalid_content, "test.jpg")
    assert is_valid is False
    assert "Invalid image file" in error


def test_validate_image_file_too_large(image_processor):
    """Test validation fails for files exceeding size limit."""
    # Create content larger than 10MB
    large_content = b"x" * (11 * 1024 * 1024)
    is_valid, error = image_processor.validate_image(large_content, "test.jpg")
    assert is_valid is False
    assert "exceeds maximum allowed size" in error


def test_convert_to_jpeg(image_processor, valid_png_bytes):
    """Test conversion from PNG to JPEG."""
    converted, format_type = image_processor.convert_to_supported_format(valid_png_bytes, target_format="JPEG")
    assert format_type == "JPEG"
    assert len(converted) > 0

    # Verify converted image is valid JPEG
    img = Image.open(io.BytesIO(converted))
    assert img.format == "JPEG"


def test_convert_to_png(image_processor, valid_jpeg_bytes):
    """Test conversion from JPEG to PNG."""
    converted, format_type = image_processor.convert_to_supported_format(valid_jpeg_bytes, target_format="PNG")
    assert format_type == "PNG"
    assert len(converted) > 0

    # Verify converted image is valid PNG
    img = Image.open(io.BytesIO(converted))
    assert img.format == "PNG"


def test_convert_rgba_to_jpeg(image_processor, valid_png_bytes):
    """Test conversion of RGBA PNG to JPEG (removes transparency)."""
    converted, format_type = image_processor.convert_to_supported_format(valid_png_bytes, target_format="JPEG")
    assert format_type == "JPEG"

    # Verify no transparency in result
    img = Image.open(io.BytesIO(converted))
    assert img.mode == "RGB"


def test_convert_invalid_format(image_processor, valid_jpeg_bytes):
    """Test conversion fails for invalid target format."""
    with pytest.raises(ValueError, match="Unsupported target format"):
        image_processor.convert_to_supported_format(valid_jpeg_bytes, target_format="BMP")


def test_convert_invalid_image(image_processor):
    """Test conversion fails for invalid image data."""
    invalid_data = b"Not an image"
    with pytest.raises(ValueError, match="Failed to convert image"):
        image_processor.convert_to_supported_format(invalid_data, target_format="JPEG")


def test_get_image_info_jpeg(image_processor, valid_jpeg_bytes):
    """Test getting information from JPEG image."""
    info = image_processor.get_image_info(valid_jpeg_bytes)

    assert info["width"] == 100
    assert info["height"] == 100
    assert info["format"] == "JPEG"
    assert info["mode"] == "RGB"
    assert info["size_bytes"] == len(valid_jpeg_bytes)


def test_get_image_info_png(image_processor, valid_png_bytes):
    """Test getting information from PNG image."""
    info = image_processor.get_image_info(valid_png_bytes)

    assert info["width"] == 100
    assert info["height"] == 100
    assert info["format"] == "PNG"
    assert info["mode"] == "RGBA"
    assert info["size_bytes"] == len(valid_png_bytes)


def test_get_image_info_invalid(image_processor):
    """Test getting info fails for invalid image."""
    invalid_data = b"Not an image"
    with pytest.raises(ValueError, match="Failed to get image info"):
        image_processor.get_image_info(invalid_data)


def test_allowed_extensions(image_processor):
    """Test all allowed extensions are validated correctly."""
    # Create a simple image
    img = Image.new("RGB", (10, 10))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    image_bytes = buffer.read()

    allowed_exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    for ext in allowed_exts:
        is_valid, _ = image_processor.validate_image(image_bytes, f"test{ext}")
        assert is_valid is True, f"Extension {ext} should be allowed"
