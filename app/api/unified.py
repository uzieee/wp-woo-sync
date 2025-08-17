"""
Unified API endpoint that routes to different functions based on JSON type attribute.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from pydantic import ValidationError

from app.models.schemas import (
    PaginationParams, 
    NormalizedResponse, 
    PaginatedResponse
)
from app.models.i18n_schemas import MultiLanguageRequest, LanguageCode
from app.services.woocommerce_service import woocommerce_service
from app.services.wordpress_service import wordpress_service
from app.services.i18n_template_service import i18n_template_service

router = APIRouter()


@router.post("/sync", response_model=NormalizedResponse)
async def unified_sync_endpoint(request: Dict[str, Any]):
    """
    Unified endpoint that routes to different functions based on 'type' attribute.
    
    Supported types:
    - 'wc_product': Create WooCommerce product
    - 'wc_order': Create WooCommerce order  
    - 'wp_post': Create WordPress post
    - 'validate_product': Validate product schema
    - 'validate_i18n': Validate i18n structure
    
    Args:
        request: JSON with 'type' attribute and corresponding data
        
    Returns:
        Response from the appropriate function
    """
    if 'type' not in request:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Missing 'type' attribute",
                "message": "Request must include 'type' field to determine routing",
                "supported_types": [
                    "wc_product", "wc_order", "wp_post", 
                    "validate_product", "validate_i18n"
                ]
            }
        )
    
    request_type = request.get('type')
    data = request.get('data', {})
    language = request.get('language', 'en')
    fallback_language = request.get('fallback_language', 'en')
    
    try:
        if request_type == 'wc_product':
            return await create_wc_product(data, language, fallback_language)
        elif request_type == 'wc_order':
            return await create_wc_order(data, language, fallback_language)
        elif request_type == 'wp_post':
            return await create_wp_post(data, language, fallback_language)
        elif request_type == 'validate_product':
            return await validate_product_schema(data)
        elif request_type == 'validate_i18n':
            return await validate_i18n_structure(data)
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Unsupported type: {request_type}",
                    "supported_types": [
                        "wc_product", "wc_order", "wp_post", 
                        "validate_product", "validate_i18n"
                    ]
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Failed to process {request_type}",
                "details": str(e)
            }
        )


@router.get("/sync", response_model=PaginatedResponse)
async def unified_get_endpoint(
    type: str = Query(..., description="Type of data to retrieve"),
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Items per page")
):
    """
    Unified GET endpoint for retrieving data.
    
    Supported types:
    - 'wc_products': Get WooCommerce products
    - 'wc_orders': Get WooCommerce orders
    - 'wp_posts': Get WordPress posts
    
    Args:
        type: Type of data to retrieve
        page: Page number
        per_page: Items per page
        
    Returns:
        Paginated response
    """
    pagination = PaginationParams(page=page, per_page=per_page)
    
    try:
        if type == 'wc_products':
            return await woocommerce_service.get_products(pagination)
        elif type == 'wc_orders':
            return await woocommerce_service.get_orders(pagination)
        elif type == 'wp_posts':
            return await wordpress_service.get_posts(pagination)
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Unsupported type: {type}",
                    "supported_types": ["wc_products", "wc_orders", "wp_posts"]
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Failed to retrieve {type}",
                "details": str(e)
            }
        )


# Helper functions for each type
async def create_wc_product(data: Dict[str, Any], language: str, fallback_language: str) -> NormalizedResponse:
    """Create WooCommerce product."""
    wc_product_data = i18n_template_service.transform_to_wc_product_i18n(data, language)
    created_product = await woocommerce_service.create_product(wc_product_data)
    
    return NormalizedResponse(
        success=True,
        data=created_product,
        message=f"WooCommerce product created successfully in {language}"
    )


async def create_wc_order(data: Dict[str, Any], language: str, fallback_language: str) -> NormalizedResponse:
    """Create WooCommerce order."""
    wc_order_data = i18n_template_service.transform_to_wc_order_i18n(data, language)
    created_order = await woocommerce_service.create_order(wc_order_data)
    
    return NormalizedResponse(
        success=True,
        data=created_order,
        message=f"WooCommerce order created successfully in {language}"
    )


async def create_wp_post(data: Dict[str, Any], language: str, fallback_language: str) -> NormalizedResponse:
    """Create WordPress post."""
    wp_post_data = i18n_template_service.transform_to_wp_post_i18n(data, language)
    created_post = await wordpress_service.create_post(wp_post_data)
    
    return NormalizedResponse(
        success=True,
        data=created_post,
        message=f"WordPress post created successfully in {language}"
    )


async def validate_product_schema(data: Dict[str, Any]) -> NormalizedResponse:
    """Validate product schema."""
    errors = []
    warnings = []
    
    # Validate i18n structure
    if "name" in data:
        try:
            from app.models.i18n_schemas import I18nData
            name_data = I18nData(**data["name"])
            warnings.append("✅ Product name i18n structure is valid")
        except ValidationError as e:
            errors.append(f"❌ Product name validation failed: {str(e)}")
    else:
        errors.append("❌ Product name is required")
    
    if "description" in data:
        try:
            from app.models.i18n_schemas import I18nData
            desc_data = I18nData(**data["description"])
            warnings.append("✅ Product description i18n structure is valid")
        except ValidationError as e:
            errors.append(f"❌ Product description validation failed: {str(e)}")
    else:
        errors.append("❌ Product description is required")
    
    # Validate price
    if "price" not in data:
        errors.append("❌ Product price is required")
    elif not isinstance(data["price"], (str, int, float)):
        errors.append("❌ Product price must be a string or number")
    
    # Validate stock quantity
    if "stock_quantity" in data:
        if not isinstance(data["stock_quantity"], int):
            errors.append("❌ Stock quantity must be an integer")
        elif data["stock_quantity"] < 0:
            errors.append("❌ Stock quantity cannot be negative")
    
    is_valid = len(errors) == 0
    
    return NormalizedResponse(
        success=is_valid,
        data={
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "validated_data": data if is_valid else None
        },
        message=f"Product validation {'passed' if is_valid else 'failed'} with {len(errors)} errors and {len(warnings)} warnings"
    )


async def validate_i18n_structure(data: Dict[str, Any]) -> NormalizedResponse:
    """Validate i18n structure."""
    errors = []
    warnings = []
    
    for field_name, field_data in data.items():
        if isinstance(field_data, dict) and any(lang in field_data for lang in ['en', 'fr', 'de', 'it', 'es']):
            try:
                from app.models.i18n_schemas import I18nData
                i18n_data = I18nData(**field_data)
                warnings.append(f"✅ {field_name} i18n structure is valid")
                
                # Check for missing translations
                missing_langs = []
                for lang in ['fr', 'de', 'it', 'es']:
                    if not hasattr(i18n_data, lang) or not getattr(i18n_data, lang):
                        missing_langs.append(lang)
                
                if missing_langs:
                    warnings.append(f"⚠️ {field_name} missing translations for: {', '.join(missing_langs)}")
                
            except ValidationError as e:
                errors.append(f"❌ {field_name} i18n validation failed: {str(e)}")
        else:
            warnings.append(f"ℹ️ {field_name} is not i18n data (single value)")
    
    is_valid = len(errors) == 0
    
    return NormalizedResponse(
        success=is_valid,
        data={
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "i18n_fields": [k for k, v in data.items() if isinstance(v, dict) and any(lang in v for lang in ['en', 'fr', 'de', 'it', 'es'])]
        },
        message=f"i18n validation {'passed' if is_valid else 'failed'} with {len(errors)} errors and {len(warnings)} warnings"
    ) 