import base64
import json
import re
from typing import Dict, Any, Optional, List
from zai import ZaiClient


class AnalyzeFoodImageUseCase:
    """Use case for analyzing food images using Z-AI SDK"""

    def __init__(self, api_key: str):
        """
        Initialize the use case with Z-AI client

        Args:
            api_key: Z-AI API key
        """
        self.client = ZaiClient(api_key=api_key)

    def _encode_image(self, image_bytes: bytes) -> str:
        """
        Encode image bytes to base64 string

        Args:
            image_bytes: Raw image bytes

        Returns:
            Base64 encoded string
        """
        return base64.b64encode(image_bytes).decode("utf-8")

    def _parse_analysis_result(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the AI response to extract food information

        Args:
            response_text: Raw response from Z-AI

        Returns:
            Dictionary containing dish_name, ingredients, and estimated_calories
        """
        # Default response if cannot identify food
        result = {
            "dish_name": "tôi không rõ",
            "ingredients": None,
            "estimated_calories": None,
            "analysis_details": response_text,
        }

        # Try to parse structured information from response
        text_lower = response_text.lower()

        # Check if AI couldn't identify the food
        unknown_patterns = [
            "không thể xác định",
            "không rõ",
            "không phải",
            "không phải là món ăn",
            "not food",
            "cannot identify",
            "unable to identify",
        ]

        if any(pattern in text_lower for pattern in unknown_patterns):
            return result

        # If response seems to contain food information, try to extract it
        if any(
            keyword in text_lower
            for keyword in ["món", "thành phần", "calo", "dish", "ingredient", "calorie"]
        ):
            # Extract dish name (usually in first line or after "món" keyword)
            lines = response_text.split("\n")
            for line in lines:
                if line.strip() and not line.startswith("-") and not line.startswith("*"):
                    # First substantial line is likely the dish name
                    result["dish_name"] = line.strip().rstrip(":：")
                    break

            # Extract ingredients
            ingredients = []
            ingredient_section = False
            for line in lines:
                line_lower = line.lower()
                if any(
                    keyword in line_lower
                    for keyword in ["thành phần", "nguyên liệu", "ingredient", "component"]
                ):
                    ingredient_section = True
                    continue
                if ingredient_section and (
                    line.strip().startswith("-") or line.strip().startswith("*")
                ):
                    ingredient = line.strip().lstrip("-*").strip()
                    if ingredient:
                        ingredients.append(ingredient)
                elif ingredient_section and line.strip() and any(
                    keyword in line.lower() for keyword in ["calo", "calorie", "kcal"]
                ):
                    ingredient_section = False

            if ingredients:
                result["ingredients"] = ingredients

            # Extract calories
            calorie_patterns = [
                r"(\d+[-~]\d+)\s*(?:kcal|calo)",
                r"(\d+)\s*(?:kcal|calo)",
                r"khoảng\s*(\d+[-~]\d+)",
                r"approximately\s*(\d+[-~]\d+)",
            ]
            for pattern in calorie_patterns:
                match = re.search(pattern, response_text, re.IGNORECASE)
                if match:
                    result["estimated_calories"] = match.group(1)
                    if "kcal" not in result["estimated_calories"].lower():
                        result["estimated_calories"] += " kcal"
                    break

        return result

    async def execute(
        self, image_bytes: bytes, content_type: str = "image/jpeg"
    ) -> Dict[str, Any]:
        """
        Analyze food image and return information about the dish

        Args:
            image_bytes: Image file content in bytes
            content_type: MIME type of the image (e.g., 'image/jpeg', 'image/png')

        Returns:
            Dictionary containing:
                - dish_name: Name of the dish or 'tôi không rõ'
                - ingredients: List of ingredients (if identifiable)
                - estimated_calories: Estimated calorie content (if available)
                - analysis_details: Full AI response

        Raises:
            Exception: If API call fails
        """
        try:
            # Encode image to base64
            image_b64 = self._encode_image(image_bytes)

            # Prepare the prompt in Vietnamese
            prompt = """Vui lòng phân tích ảnh món ăn này và cung cấp thông tin sau:

1. Tên món ăn (nếu không xác định được, hãy trả lời "tôi không rõ")
2. Thành phần món ăn (liệt kê các nguyên liệu chính)
3. Ước tính khối lượng calo

Định dạng câu trả lời:

Tên món: [tên món ăn]

Thành phần:
- [nguyên liệu 1]
- [nguyên liệu 2]
- ...

Calo ước tính: [số calo] kcal

Nếu đây không phải là món ăn hoặc không thể xác định, vui lòng chỉ trả lời "tôi không rõ"."""

            # Call Z-AI API
            response = self.client.chat.completions.create(
                model="glm-4v",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{content_type};base64,{image_b64}"},
                            },
                        ],
                    }
                ],
            )

            # Extract response text
            response_text = response.choices[0].message.content

            # Parse and structure the response
            result = self._parse_analysis_result(response_text)

            return result

        except Exception as e:
            raise Exception(f"Failed to analyze image: {str(e)}")
