"""Z-AI service for image upload and processing."""
import base64
from typing import Optional

from zai import ZaiClient


class ZaiService:
    """Service for interacting with Z-AI API."""

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize Z-AI service.

        Args:
            api_key: Z-AI API key
            base_url: Optional custom base URL for Z-AI API
        """
        self.client = ZaiClient(
            api_key=api_key,
            base_url=base_url if base_url else "https://api.z.ai/api/paas/v4/",
        )

    async def upload_food_image(self, image_bytes: bytes, image_format: str) -> dict:
        """
        Upload food image to Z-AI for analysis.

        Args:
            image_bytes: Image binary data
            image_format: Image format ('JPEG' or 'PNG')

        Returns:
            Dictionary containing Z-AI response with image analysis

        Raises:
            Exception: If upload or analysis fails
        """
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            # Determine MIME type
            mime_type = f"image/{image_format.lower()}"
            if image_format.upper() == "JPEG":
                mime_type = "image/jpeg"

            # Create data URL
            image_data_url = f"data:{mime_type};base64,{image_base64}"

            # Call Z-AI API with multimodal chat
            response = self.client.chat.completions.create(
                model="glm-4v",  # Vision model for image analysis
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this food image. Identify the dish name, ingredients, estimated calories, and provide a brief description.",
                            },
                            {"type": "image_url", "image_url": {"url": image_data_url}},
                        ],
                    }
                ],
            )

            # Extract analysis result
            analysis = response.choices[0].message.content if response.choices else "No analysis available"

            return {
                "success": True,
                "analysis": analysis,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                },
            }

        except Exception as e:
            raise Exception(f"Failed to upload image to Z-AI: {str(e)}")

    async def analyze_food_image_stream(self, image_bytes: bytes, image_format: str):
        """
        Upload food image to Z-AI for streaming analysis.

        Args:
            image_bytes: Image binary data
            image_format: Image format ('JPEG' or 'PNG')

        Yields:
            Streaming chunks of analysis text

        Raises:
            Exception: If upload or analysis fails
        """
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

            # Determine MIME type
            mime_type = f"image/{image_format.lower()}"
            if image_format.upper() == "JPEG":
                mime_type = "image/jpeg"

            # Create data URL
            image_data_url = f"data:{mime_type};base64,{image_base64}"

            # Call Z-AI API with streaming
            response = self.client.chat.completions.create(
                model="glm-4v",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this food image. Identify the dish name, ingredients, estimated calories, and provide a brief description.",
                            },
                            {"type": "image_url", "image_url": {"url": image_data_url}},
                        ],
                    }
                ],
                stream=True,
            )

            # Stream response
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise Exception(f"Failed to stream analysis from Z-AI: {str(e)}")
