"""
WooCommerce API router for products and orders.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any

from app.models.schemas import (
    PaginationParams, 
    ClientRequest, 
    NormalizedResponse, 
    PaginatedResponse
)
from app.services.woocommerce_service import woocommerce_service
from app.services.template_service import template_service

router = APIRouter()


@router.get("/products", response_model=PaginatedResponse)
async def get_products(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page")
):
    """
    Get WooCommerce products with pagination.
    
    Args:
        page: Page number (default: 1)
        per_page: Items per page (default: 10, max: 100)
        
    Returns:
        Paginated products response
    """
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
async def create_product(request: ClientRequest):
    """
    Create a new WooCommerce product from client JSON.
    
    Args:
        request: Client JSON data to transform and create product
        
    Returns:
        Created product data
    """
    try:
        wc_product_data = template_service.transform_to_wc_product(request.data)
        created_product = await woocommerce_service.create_product(wc_product_data)
        
        return NormalizedResponse(
            success=True,
            data=created_product,
            message="Product created successfully"
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
    """
    Get WooCommerce orders with pagination.
    
    Args:
        page: Page number (default: 1)
        per_page: Items per page (default: 10, max: 100)
        
    Returns:
        Paginated orders response
    """
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
async def create_order(request: ClientRequest):
    """
    Create a new WooCommerce order from client JSON.
    
    Args:
        request: Client JSON data to transform and create order
        
    Returns:
        Created order data
    """
    try:
        wc_order_data = template_service.transform_to_wc_order(request.data)
        created_order = await woocommerce_service.create_order(wc_order_data)
        
        return NormalizedResponse(
            success=True,
            data=created_order,
            message="Order created successfully"
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