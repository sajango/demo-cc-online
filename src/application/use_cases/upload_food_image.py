"""Use case for uploading and analyzing food images with Z-AI."""
from typing import Tuple

from src.infrastructure.services.image_processor import ImageProcessorService
from src.infrastructure.services.zai_service import ZaiService


class UploadFoodImageUseCase:
    """Use case for uploading and analyzing food images."""

    def __init__(
        self,
        image_processor: ImageProcessorService,
        zai_service: ZaiService,
    ):
        """
        Initialize use case with dependencies.

        Args:
            image_processor: Service for image validation and processing
            zai_service: Service for Z-AI API integration
        """
        self.image_processor = image_processor
        self.zai_service = zai_service

    async def execute(self, file_content: bytes, filename: str, target_format: str = "JPEG") -> dict:
        """
        Execute food image upload and analysis.

        Args:
            file_content: Binary content of uploaded image
            filename: Original filename
            target_format: Target image format ('JPEG' or 'PNG'), defaults to 'JPEG'

        Returns:
            Dictionary containing:
                - success: Boolean indicating success
                - message: Success or error message
                - image_info: Information about the processed image
                - analysis: Z-AI analysis results (if successful)

        Raises:
            ValueError: If validation fails or processing error occurs
        """
        # Step 1: Validate image
        is_valid, error_message = self.image_processor.validate_image(file_content, filename)
        if not is_valid:
            raise ValueError(f"Image validation failed: {error_message}")

        # Step 2: Get original image info
        try:
            original_info = self.image_processor.get_image_info(file_content)
        except Exception as e:
            raise ValueError(f"Failed to read image information: {str(e)}")

        # Step 3: Convert to supported format (JPG or PNG)
        try:
            converted_bytes, final_format = self.image_processor.convert_to_supported_format(
                file_content, target_format=target_format
            )
        except Exception as e:
            raise ValueError(f"Failed to convert image: {str(e)}")

        # Step 4: Upload to Z-AI for analysis
        try:
            zai_result = await self.zai_service.upload_food_image(converted_bytes, final_format)
        except Exception as e:
            raise ValueError(f"Failed to analyze image with Z-AI: {str(e)}")

        # Step 5: Return comprehensive result
        return {
            "success": True,
            "message": "Image uploaded and analyzed successfully",
            "image_info": {
                "original_filename": filename,
                "original_format": original_info.get("format"),
                "converted_format": final_format,
                "width": original_info.get("width"),
                "height": original_info.get("height"),
                "original_size_bytes": original_info.get("size_bytes"),
                "converted_size_bytes": len(converted_bytes),
            },
            "analysis": zai_result.get("analysis"),
            "zai_metadata": {
                "model": zai_result.get("model"),
                "usage": zai_result.get("usage"),
            },
        }

    async def execute_streaming(
        self, file_content: bytes, filename: str, target_format: str = "JPEG"
    ) -> Tuple[dict, any]:
        """
        Execute food image upload with streaming analysis.

        Args:
            file_content: Binary content of uploaded image
            filename: Original filename
            target_format: Target image format ('JPEG' or 'PNG')

        Returns:
            Tuple of (image_info_dict, streaming_generator)

        Raises:
            ValueError: If validation fails or processing error occurs
        """
        # Step 1: Validate image
        is_valid, error_message = self.image_processor.validate_image(file_content, filename)
        if not is_valid:
            raise ValueError(f"Image validation failed: {error_message}")

        # Step 2: Get original image info
        try:
            original_info = self.image_processor.get_image_info(file_content)
        except Exception as e:
            raise ValueError(f"Failed to read image information: {str(e)}")

        # Step 3: Convert to supported format
        try:
            converted_bytes, final_format = self.image_processor.convert_to_supported_format(
                file_content, target_format=target_format
            )
        except Exception as e:
            raise ValueError(f"Failed to convert image: {str(e)}")

        # Step 4: Prepare image info
        image_info = {
            "original_filename": filename,
            "original_format": original_info.get("format"),
            "converted_format": final_format,
            "width": original_info.get("width"),
            "height": original_info.get("height"),
            "original_size_bytes": original_info.get("size_bytes"),
            "converted_size_bytes": len(converted_bytes),
        }

        # Step 5: Get streaming generator
        try:
            stream_generator = self.zai_service.analyze_food_image_stream(converted_bytes, final_format)
        except Exception as e:
            raise ValueError(f"Failed to start streaming analysis: {str(e)}")

        return image_info, stream_generator
