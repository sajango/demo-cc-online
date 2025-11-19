from pydantic import BaseModel, Field
from typing import Optional, List


class FoodAnalysisResponse(BaseModel):
    """Schema for food analysis response"""

    dish_name: str = Field(..., description="Tên món ăn (hoặc 'tôi không rõ' nếu không xác định được)")
    ingredients: Optional[List[str]] = Field(
        None, description="Danh sách thành phần món ăn"
    )
    estimated_calories: Optional[str] = Field(
        None, description="Ước tính khối lượng calo"
    )
    analysis_details: Optional[str] = Field(
        None, description="Thông tin chi tiết về phân tích"
    )


class ErrorResponse(BaseModel):
    """Schema for error response"""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
