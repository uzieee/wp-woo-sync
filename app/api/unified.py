from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import ValidationError

from app.models.schemas import NormalizedResponse
from app.services.woocommerce_service import woocommerce_service
from app.services.wordpress_service import wordpress_service
from app.services.i18n_template_service import i18n_template_service

router = APIRouter()


@router.post("/sync", response_model=NormalizedResponse)
async def unified_sync_endpoint(request: Dict[str, Any]):
    if 'action_id' not in request:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Missing 'action_id' attribute",
                "message": "Request must include 'action_id' field to determine routing",
                "supported_action_ids": [
                    "create_wc_product", "create_wc_order", "create_wp_post", 
                    "validate_product", "validate_i18n"
                ]
            }
        )
    
    action_id = request.get('action_id')
    data = request.get('data', {})
    language = request.get('language', 'en')
    fallback_language = request.get('fallback_language', 'en')
    
    try:
        if action_id == 'create_wc_product':
            return await create_wc_product(data, language, fallback_language)
        elif action_id == 'create_wc_order':
            return await create_wc_order(data, language, fallback_language)
        elif action_id == 'create_wp_post':
            return await create_wp_post(data, language, fallback_language)
        elif action_id == 'validate_product':
            return await validate_product_schema(data)
        elif action_id == 'validate_i18n':
            return await validate_i18n_structure(data)
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Unsupported action_id: {action_id}",
                    "supported_action_ids": [
                        "create_wc_product", "create_wc_order", "create_wp_post", 
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
                "error": f"Failed to process action_id: {action_id}",
                "details": str(e)
            }
        )


async def create_wc_product(data: Dict[str, Any], language: str, fallback_language: str) -> NormalizedResponse:
    wc_product_data = i18n_template_service.transform_to_wc_product_i18n(data, language)
    created_product = await woocommerce_service.create_product(wc_product_data)
    
    return NormalizedResponse(
        success=True,
        data=created_product,
        message=f"WooCommerce product created successfully in {language}"
    )


async def create_wc_order(data: Dict[str, Any], language: str, fallback_language: str) -> NormalizedResponse:
    wc_order_data = i18n_template_service.transform_to_wc_order_i18n(data, language)
    created_order = await woocommerce_service.create_order(wc_order_data)
    
    return NormalizedResponse(
        success=True,
        data=created_order,
        message=f"WooCommerce order created successfully in {language}"
    )


async def create_wp_post(data: Dict[str, Any], language: str, fallback_language: str) -> NormalizedResponse:
    wp_post_data = i18n_template_service.transform_to_wp_post_i18n(data, language)
    created_post = await wordpress_service.create_post(wp_post_data)
    
    return NormalizedResponse(
        success=True,
        data=created_post,
        message=f"WordPress post created successfully in {language}"
    )


async def validate_product_schema(data: Dict[str, Any]) -> NormalizedResponse:
    errors = []
    warnings = []
    
    if "name" in data:
        try:
            from app.models.i18n_schemas import I18nData
            name_data = I18nData(**data["name"])
            warnings.append("Product name i18n structure is valid")
        except ValidationError as e:
            errors.append(f"Product name validation failed: {str(e)}")
    else:
        errors.append("Product name is required")
    
    if "description" in data:
        try:
            from app.models.i18n_schemas import I18nData
            desc_data = I18nData(**data["description"])
            warnings.append("Product description i18n structure is valid")
        except ValidationError as e:
            errors.append(f"Product description validation failed: {str(e)}")
    else:
        errors.append("Product description is required")
    
    if "price" not in data:
        errors.append("Product price is required")
    elif not isinstance(data["price"], (str, int, float)):
        errors.append("Product price must be a string or number")
    
    if "stock_quantity" in data:
        if not isinstance(data["stock_quantity"], int):
            errors.append("Stock quantity must be an integer")
        elif data["stock_quantity"] < 0:
            errors.append("Stock quantity cannot be negative")
    
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
    errors = []
    warnings = []
    
    for field_name, field_data in data.items():
        if isinstance(field_data, dict) and any(lang in field_data for lang in ['en', 'fr', 'de', 'it', 'es']):
            try:
                from app.models.i18n_schemas import I18nData
                i18n_data = I18nData(**field_data)
                warnings.append(f"{field_name} i18n structure is valid")
                
                missing_langs = []
                for lang in ['fr', 'de', 'it', 'es']:
                    if not hasattr(i18n_data, lang) or not getattr(i18n_data, lang):
                        missing_langs.append(lang)
                
                if missing_langs:
                    warnings.append(f"{field_name} missing translations for: {', '.join(missing_langs)}")
                
            except ValidationError as e:
                errors.append(f"{field_name} i18n validation failed: {str(e)}")
        else:
            warnings.append(f"{field_name} is not i18n data (single value)")
    
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