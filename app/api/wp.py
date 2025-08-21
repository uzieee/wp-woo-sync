from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

from app.models.schemas import (
    PaginationParams, 
    ClientRequest, 
    NormalizedResponse, 
    PaginatedResponse
)
from app.models.i18n_schemas import MultiLanguageRequest, LanguageCode
from app.services.wordpress_service import wordpress_service
from app.services.template_service import template_service
from app.services.i18n_template_service import i18n_template_service

router = APIRouter()


@router.get("/posts", response_model=PaginatedResponse)
async def get_posts(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page")
):
    try:
        pagination = PaginationParams(page=page, per_page=per_page)
        result = await wordpress_service.get_posts(pagination)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to fetch posts",
                "details": str(e)
            }
        )


@router.post("/posts", response_model=NormalizedResponse)
async def create_post(request: MultiLanguageRequest):
    try:
        wp_post_data = i18n_template_service.transform_to_wp_post_i18n(
            request.data, 
            request.language.value
        )
        
        created_post = await wordpress_service.create_post(wp_post_data)
        
        return NormalizedResponse(
            success=True,
            data=created_post,
            message=f"Post created successfully in {request.language.value}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Template transformation failed",
                "details": str(e)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to create post",
                "details": str(e)
            }
        ) 