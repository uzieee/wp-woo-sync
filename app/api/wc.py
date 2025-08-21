from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

from app.models.schemas import (
    PaginationParams, 
    ClientRequest, 
    NormalizedResponse, 
    PaginatedResponse
)
from app.models.i18n_schemas import MultiLanguageRequest, LanguageCode
from app.services.woocommerce_service import woocommerce_service
from app.services.template_service import template_service
from app.services.i18n_template_service import i18n_template_service

router = APIRouter()


@router.get("/products", response_model=PaginatedResponse)
async def get_products(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page")
):
    try:
        pagination = PaginationParams(page=page, per_page=per_page)
        result = await woocommerce_service.get_products(pagination)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to fetch products",
                "details": str(e)
            }
        )


@router.post("/products", response_model=NormalizedResponse)
async def create_product(request: MultiLanguageRequest):
    try:
        wc_product_data = i18n_template_service.transform_to_wc_product_i18n(
            request.data, 
            request.language.value
        )
        
        created_product = await woocommerce_service.create_product(wc_product_data)
        
        return NormalizedResponse(
            success=True,
            data=created_product,
            message=f"Product created successfully in {request.language.value}"
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
                "error": "Failed to create product",
                "details": str(e)
            }
        )


@router.get("/orders", response_model=PaginatedResponse)
async def get_orders(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page")
):
    try:
        pagination = PaginationParams(page=page, per_page=per_page)
        result = await woocommerce_service.get_orders(pagination)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to fetch orders",
                "details": str(e)
            }
        )


@router.post("/orders", response_model=NormalizedResponse)
async def create_order(request: MultiLanguageRequest):
    try:
        wc_order_data = i18n_template_service.transform_to_wc_order_i18n(
            request.data, 
            request.language.value
        )
        
        created_order = await woocommerce_service.create_order(wc_order_data)
        
        return NormalizedResponse(
            success=True,
            data=created_order,
            message=f"Order created successfully in {request.language.value}"
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
                "error": "Failed to create order",
                "details": str(e)
            }
        ) 