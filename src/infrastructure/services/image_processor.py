"""Image processing service for validation and conversion."""
import io
from typing import Tuple

from PIL import Image


class ImageProcessorService:
    """Service for image validation and format conversion."""

    ALLOWED_MIME_TYPES = {
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/gif",
        "image/bmp",
        "image/webp",
    }

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def validate_image(self, file_content: bytes, filename: str) -> Tuple[bool, str]:
        """
        Validate if uploaded file is a valid image.

        Args:
            file_content: Binary content of the uploaded file
            filename: Original filename

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file size
        if len(file_content) > self.MAX_FILE_SIZE:
            return False, f"File size exceeds maximum allowed size of {self.MAX_FILE_SIZE / (1024 * 1024)}MB"

        # Check file extension
        file_ext = filename.lower().split(".")[-1] if "." in filename else ""
        if f".{file_ext}" not in self.ALLOWED_EXTENSIONS:
            return False, f"File extension '.{file_ext}' is not allowed. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"

        # Validate image format by trying to open it
        try:
            with Image.open(io.BytesIO(file_content)) as img:
                # Verify the image
                img.verify()
                return True, ""
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"

    def convert_to_supported_format(
        self, file_content: bytes, target_format: str = "JPEG"
    ) -> Tuple[bytes, str]:
        """
        Convert image to JPG or PNG format.

        Args:
            file_content: Binary content of the image
            target_format: Target format ('JPEG' or 'PNG')

        Returns:
            Tuple of (converted_image_bytes, format)

        Raises:
            ValueError: If target format is not supported or conversion fails
        """
        if target_format.upper() not in ["JPEG", "PNG"]:
            raise ValueError(f"Unsupported target format: {target_format}. Use 'JPEG' or 'PNG'")

        try:
            # Open the image
            with Image.open(io.BytesIO(file_content)) as img:
                # Convert RGBA to RGB for JPEG (JPEG doesn't support transparency)
                if target_format.upper() == "JPEG" and img.mode in ("RGBA", "LA", "P"):
                    # Create white background
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                    img = background
                elif target_format.upper() == "PNG" and img.mode not in ("RGBA", "RGB", "L"):
                    img = img.convert("RGBA")

                # Save to bytes
                output = io.BytesIO()
                img.save(output, format=target_format.upper(), quality=95 if target_format.upper() == "JPEG" else None)
                output.seek(0)

                return output.read(), target_format.upper()

        except Exception as e:
            raise ValueError(f"Failed to convert image: {str(e)}")

    def get_image_info(self, file_content: bytes) -> dict:
        """
        Get image information (dimensions, format, mode).

        Args:
            file_content: Binary content of the image

        Returns:
            Dictionary with image information
        """
        try:
            with Image.open(io.BytesIO(file_content)) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                    "size_bytes": len(file_content),
                }
        except Exception as e:
            raise ValueError(f"Failed to get image info: {str(e)}")
