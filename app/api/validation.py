from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from typing import Dict, Any, List

from app.models.i18n_schemas import I18nData, I18nTranslation, MultiLanguageRequest
from app.models.schemas import NormalizedResponse

router = APIRouter()


@router.post("/validate-product", response_model=NormalizedResponse)
async def validate_product_schema(data: Dict[str, Any]):
    errors = []
    warnings = []
    
    if "name" in data:
        try:
            name_data = I18nData(**data["name"])
            warnings.append("Product name i18n structure is valid")
        except ValidationError as e:
            errors.append(f"Product name validation failed: {str(e)}")
    else:
        errors.append("Product name is required")
    
    if "description" in data:
        try:
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
    
    if "categories" in data:
        if not isinstance(data["categories"], list):
            errors.append("Categories must be a list")
        else:
            for i, cat in enumerate(data["categories"]):
                if not isinstance(cat, dict):
                    errors.append(f"Category {i} must be an object")
                elif "id" not in cat or "name" not in cat:
                    errors.append(f"Category {i} must have 'id' and 'name' fields")
    
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
        message=f"Validation {'passed' if is_valid else 'failed'} with {len(errors)} errors and {len(warnings)} warnings"
    )


@router.post("/validate-i18n", response_model=NormalizedResponse)
async def validate_i18n_structure(data: Dict[str, Any]):
    errors = []
    warnings = []
    
    for field_name, field_data in data.items():
        if isinstance(field_data, dict) and any(lang in field_data for lang in ['en', 'fr', 'de', 'it', 'es']):
            try:
                i18n_data = I18nData(**field_data)
                warnings.append(f"{field_name} i18n structure is valid")
                
                missing_langs = []
                for lang in ['fr', 'de', 'it', 'es']:
                    if not hasattr(i18n_data, lang) or not getattr(i18n_data, lang):
                        missing_langs.append(lang)
                
                if missing_langs:
                    warnings.append(f"{field_name} missing translations for: {', '.join(missing_langs)}")
                
                for lang in ['en', 'fr', 'de', 'it', 'es']:
                    lang_data = getattr(i18n_data, lang, None)
                    if lang_data and hasattr(lang_data, 'limit') and lang_data.limit:
                        if len(lang_data.translation) > lang_data.limit:
                            errors.append(f"{field_name} {lang} translation exceeds {lang_data.limit} character limit")
                
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


@router.get("/schema-examples")
async def get_schema_examples():
    return {
        "valid_product_example": {
            "name": {
                "en": {"translation": "BMW X5", "notes": "Product name", "limit": 50},
                "fr": {"translation": "BMW X5", "notes": "Nom du produit", "limit": 50}
            },
            "description": {
                "en": {"translation": "Luxury SUV", "notes": "Product description", "limit": 500},
                "fr": {"translation": "SUV de luxe", "notes": "Description du produit", "limit": 500}
            },
            "price": "89,500",
            "stock_quantity": 3
        },
        "invalid_product_example": {
            "name": {
                "en": {"translation": "BMW X5", "notes": "Product name"}
            },
            "price": "invalid_price",
            "stock_quantity": -5
        },
        "validation_rules": {
            "required_fields": ["name", "description", "price"],
            "i18n_required": ["en translation"],
            "data_types": {
                "price": "string or number",
                "stock_quantity": "integer >= 0",
                "categories": "array of objects with id and name"
            },
            "i18n_structure": {
                "translation": "required string",
                "notes": "optional string",
                "context": "optional string", 
                "limit": "optional integer"
            }
        }
    } 