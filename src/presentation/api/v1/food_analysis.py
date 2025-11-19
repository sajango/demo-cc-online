from fastapi import APIRouter, File, UploadFile, HTTPException, status
from typing import Optional

from src.core.config import settings
from src.presentation.schemas.food_schema import FoodAnalysisResponse, ErrorResponse
from src.application.use_cases.analyze_food_image import AnalyzeFoodImageUseCase

router = APIRouter(prefix="/food-analysis", tags=["food-analysis"])


@router.post(
    "/analyze",
    response_model=FoodAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def analyze_food_image(file: UploadFile = File(...)):
    """
    Analyze a food image and return dish information

    Upload an image of food to get:
    - Dish name (or 'tôi không rõ' if unidentifiable)
    - Ingredients list
    - Estimated calorie content

    Args:
        file: Image file (JPEG, PNG, etc.)

    Returns:
        FoodAnalysisResponse with dish information
    """
    # Validate Z-AI API key is configured
    if not settings.ZAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Z-AI API key is not configured. Please set ZAI_API_KEY in environment variables.",
        )

    # Validate file type
    allowed_content_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_content_types)}",
        )

    # Validate file size (max 10MB)
    max_file_size = 10 * 1024 * 1024  # 10MB in bytes
    file_content = await file.read()
    if len(file_content) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 10MB",
        )

    try:
        # Initialize use case with API key
        use_case = AnalyzeFoodImageUseCase(api_key=settings.ZAI_API_KEY)

        # Analyze the image
        result = await use_case.execute(
            image_bytes=file_content, content_type=file.content_type
        )

        return FoodAnalysisResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze image: {str(e)}",
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for food analysis service"""
    api_key_configured = bool(settings.ZAI_API_KEY)
    return {
        "status": "healthy" if api_key_configured else "degraded",
        "api_key_configured": api_key_configured,
        "message": "Food analysis service is running"
        if api_key_configured
        else "Z-AI API key not configured",
    }
