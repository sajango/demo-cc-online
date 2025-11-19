"""Pydantic schemas for food image upload API."""
from typing import Optional

from pydantic import BaseModel, Field


class ImageInfoResponse(BaseModel):
    """Image information in response."""

    original_filename: str = Field(..., description="Original uploaded filename")
    original_format: Optional[str] = Field(None, description="Original image format")
    converted_format: str = Field(..., description="Final converted format (JPEG or PNG)")
    width: int = Field(..., description="Image width in pixels")
    height: int = Field(..., description="Image height in pixels")
    original_size_bytes: int = Field(..., description="Original file size in bytes")
    converted_size_bytes: int = Field(..., description="Converted file size in bytes")


class ZaiUsageInfo(BaseModel):
    """Z-AI token usage information."""

    prompt_tokens: int = Field(0, description="Number of tokens in prompt")
    completion_tokens: int = Field(0, description="Number of tokens in completion")
    total_tokens: int = Field(0, description="Total tokens used")


class ZaiMetadata(BaseModel):
    """Z-AI metadata information."""

    model: str = Field(..., description="Z-AI model used for analysis")
    usage: ZaiUsageInfo = Field(..., description="Token usage information")


class FoodImageUploadResponse(BaseModel):
    """Response for food image upload and analysis."""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Success or error message")
    image_info: ImageInfoResponse = Field(..., description="Information about the processed image")
    analysis: str = Field(..., description="Z-AI analysis of the food image")
    zai_metadata: ZaiMetadata = Field(..., description="Z-AI request metadata")

    model_config = {"json_schema_extra": {"example": {
        "success": True,
        "message": "Image uploaded and analyzed successfully",
        "image_info": {
            "original_filename": "food_photo.jpg",
            "original_format": "JPEG",
            "converted_format": "JPEG",
            "width": 1920,
            "height": 1080,
            "original_size_bytes": 524288,
            "converted_size_bytes": 512000,
        },
        "analysis": "This is a plate of Pad Thai, a popular Thai stir-fried noodle dish...",
        "zai_metadata": {"model": "glm-4v", "usage": {"prompt_tokens": 150, "completion_tokens": 200, "total_tokens": 350}},
    }}}


class ErrorResponse(BaseModel):
    """Error response schema."""

    success: bool = Field(False, description="Always False for errors")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")

    model_config = {"json_schema_extra": {"example": {
        "success": False,
        "message": "Image validation failed",
        "detail": "File size exceeds maximum allowed size of 10MB",
    }}}
