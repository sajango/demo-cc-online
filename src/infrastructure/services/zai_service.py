"""Z-AI service for image upload and processing."""
import base64
import json
from typing import Optional, Dict, Any, List

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

    def convert_text_to_analysis_data(self, input_text: str) -> Dict[str, Any]:
        start_tag = "<|begin_of_box|>"
        end_tag = "<|end_of_box|>"

        json_string: str = ""
        parsed_data: Optional[Dict[str, Any]] = None
        has_box_tags = start_tag in input_text and end_tag in input_text

        if has_box_tags:
            try:
                json_start_index = input_text.find(start_tag) + len(start_tag)
                json_end_index = input_text.rfind(end_tag)

                if json_end_index > json_start_index:
                    json_string = input_text[json_start_index:json_end_index].strip()
            except Exception:
                json_string = ""
        else:
            json_string = input_text.strip()
        if json_string:
            try:
                parsed_data = json.loads(json_string)
                if not isinstance(parsed_data, dict):
                    parsed_data = None

            except json.JSONDecodeError:
                pass
        analysis_text: str = parsed_data.get("description", input_text) if parsed_data else input_text

        if parsed_data:
            analysis_data = {
                "dish_name": parsed_data.get("dish_name", "Unknown"),
                "ingredients": parsed_data.get("ingredients", []),
                "estimated_calories": parsed_data.get("estimated_calories", "N/A"),
                "description": analysis_text,
                "confidence": parsed_data.get("confidence", "low")
            }
        else:
            analysis_data = {
                "dish_name": "Unknown",
                "ingredients": [],
                "estimated_calories": "N/A",
                "description": analysis_text,
                "confidence": "low"
            }

        return analysis_data

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
                model="glm-4.5v",  # Vision model for image analysis
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this food image and provide a structured JSON response with the following format:
{
    "dish_name": "Name of the dish in Vietnamese",
    "ingredients": ["ingredient1", "ingredient2", ...],
    "estimated_calories": "calorie range (e.g., 450-550 kcal)",
    "description": "Brief description of the dish in Vietnamese",
    "confidence": "high/medium/low"
}

Only return the JSON object, no additional text.""",
                            },
                            {"type": "image_url", "image_url": {"url": image_data_url}},
                        ],
                    }
                ],
                temperature=0.5,
                max_tokens=2000,
            )

            # Extract analysis result
            analysis_text = response.choices[0].message.content if response.choices else "{}"

            # Parse JSON response
            try:
                print(analysis_text)
                analysis_data = self.convert_text_to_analysis_data(input_text=analysis_text)
                print(analysis_data)
            except json.JSONDecodeError:
                # Fallback if response is not valid JSON
                analysis_data = {
                    "dish_name": "Unknown",
                    "ingredients": [],
                    "estimated_calories": "N/A",
                    "description": analysis_text,
                    "confidence": "low"
                }

            return {
                "success": True,
                "analysis": analysis_data,
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
