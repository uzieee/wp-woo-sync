"""
Pydantic schemas for request/response models.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=10, ge=1, le=100, description="Items per page")


class ClientRequest(BaseModel):
    """Arbitrary client JSON request."""
    data: Dict[str, Any] = Field(..., description="Client data to transform")


class NormalizedResponse(BaseModel):
    """Normalized response for clients."""
    success: bool = Field(..., description="Operation success status")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    errors: Optional[List[str]] = Field(None, description="Error messages")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    items: List[Dict[str, Any]] = Field(..., description="List of items")
    pagination: Dict[str, Any] = Field(..., description="Pagination metadata")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(default=False, description="Operation success status")
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details") 