"""API endpoints for food image upload and analysis (no authentication required)."""
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from src.application.use_cases.upload_food_image import UploadFoodImageUseCase
from src.core.dependencies import get_image_processor_service, get_zai_service
from src.presentation.schemas.food_image_schema import ErrorResponse, FoodImageUploadResponse

router = APIRouter(prefix="/food-images", tags=["Food Images"])


@router.post(
    "/upload",
    response_model=FoodImageUploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload food image for AI analysis",
    description="""
    Upload a food image for analysis using Z-AI.

    **No authentication required** - This is a public endpoint.

    **Process:**
    1. Validates uploaded file is an image
    2. Converts image to JPEG or PNG format
    3. Sends to Z-AI for food analysis
    4. Returns analysis results with image information

    **Supported formats:** JPEG, PNG, GIF, BMP, WebP
    **Max file size:** 10MB
    **Converted to:** JPEG (default) or PNG
    """,
    responses={
        200: {"description": "Image uploaded and analyzed successfully", "model": FoodImageUploadResponse},
        400: {"description": "Invalid image or validation error", "model": ErrorResponse},
        500: {"description": "Server error during processing", "model": ErrorResponse},
    },
)
async def upload_food_image(
    file: UploadFile = File(..., description="Food image file to upload and analyze"),
    target_format: str = "JPEG",
) -> FoodImageUploadResponse:
    """
    Upload and analyze a food image.

    Args:
        file: Uploaded image file
        target_format: Target conversion format ('JPEG' or 'PNG'), defaults to 'JPEG'

    Returns:
        Analysis results with image information

    Raises:
        HTTPException: If validation fails or processing error occurs
    """
    # Validate target format
    if target_format.upper() not in ["JPEG", "PNG"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": "Invalid target format", "detail": "Target format must be 'JPEG' or 'PNG'"},
        )

    # Read file content
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": "Failed to read uploaded file", "detail": str(e)},
        )

    # Create use case with dependencies
    image_processor = get_image_processor_service()
    zai_service = get_zai_service()
    use_case = UploadFoodImageUseCase(image_processor, zai_service)

    # Execute use case
    try:
        result = await use_case.execute(
            file_content=file_content, filename=file.filename or "unknown.jpg", target_format=target_format.upper()
        )
        return FoodImageUploadResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": "Validation or processing error", "detail": str(e)},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": "Internal server error", "detail": str(e)},
        )


@router.post(
    "/upload/stream",
    status_code=status.HTTP_200_OK,
    summary="Upload food image with streaming analysis",
    description="""
    Upload a food image and receive streaming analysis results from Z-AI.

    **No authentication required** - This is a public endpoint.

    This endpoint streams the analysis results as they are generated,
    providing a better user experience for real-time analysis.

    **Supported formats:** JPEG, PNG, GIF, BMP, WebP
    **Max file size:** 10MB
    """,
)
async def upload_food_image_stream(
    file: UploadFile = File(..., description="Food image file to upload and analyze"),
    target_format: str = "JPEG",
) -> StreamingResponse:
    """
    Upload and analyze a food image with streaming response.

    Args:
        file: Uploaded image file
        target_format: Target conversion format ('JPEG' or 'PNG')

    Returns:
        Streaming response with analysis results

    Raises:
        HTTPException: If validation fails or processing error occurs
    """
    # Validate target format
    if target_format.upper() not in ["JPEG", "PNG"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": "Invalid target format", "detail": "Target format must be 'JPEG' or 'PNG'"},
        )

    # Read file content
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": "Failed to read uploaded file", "detail": str(e)},
        )

    # Create use case with dependencies
    image_processor = get_image_processor_service()
    zai_service = get_zai_service()
    use_case = UploadFoodImageUseCase(image_processor, zai_service)

    # Execute streaming use case
    try:
        image_info, stream_generator = await use_case.execute_streaming(
            file_content=file_content, filename=file.filename or "unknown.jpg", target_format=target_format.upper()
        )

        # Define streaming response generator
        async def generate():
            # First send image info as JSON
            import json

            yield f"data: {json.dumps({'type': 'image_info', 'data': image_info})}\n\n"

            # Then stream analysis
            async for chunk in stream_generator:
                yield f"data: {json.dumps({'type': 'analysis_chunk', 'data': chunk})}\n\n"

            # Send completion marker
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": "Validation or processing error", "detail": str(e)},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": "Internal server error", "detail": str(e)},
        )
