"""
i18n JSON schemas for multi-language support.
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, List
from enum import Enum


class LanguageCode(str, Enum):
    """Supported language codes."""
    EN = "en"
    FR = "fr"
    DE = "de"
    IT = "it"
    ES = "es"


class I18nTranslation(BaseModel):
    """i18n translation structure."""
    translation: str = Field(..., description="The actual translation")
    notes: Optional[str] = Field(None, description="Description of the key")
    context: Optional[str] = Field(None, description="Context of the key")
    limit: Optional[int] = Field(None, description="Character limit of the key")


class I18nData(BaseModel):
    """i18n data structure for multi-language content."""
    en: I18nTranslation = Field(..., description="English translation")
    fr: Optional[I18nTranslation] = Field(None, description="French translation")
    de: Optional[I18nTranslation] = Field(None, description="German translation")
    it: Optional[I18nTranslation] = Field(None, description="Italian translation")
    es: Optional[I18nTranslation] = Field(None, description="Spanish translation")

    @validator('en')
    def validate_english_required(cls, v):
        if not v or not v.translation:
            raise ValueError("English translation is required")
        return v

    def get_translation(self, lang: str) -> str:
        """Get translation for specific language with fallback to English."""
        if lang == "en":
            return self.en.translation
        
        # Try to get the requested language
        lang_data = getattr(self, lang, None)
        if lang_data and lang_data.translation:
            return lang_data.translation
        
        # Fallback to English
        return self.en.translation


class MultiLanguageRequest(BaseModel):
    """Multi-language request structure."""
    data: Dict[str, Any] = Field(..., description="Client data to transform")
    language: LanguageCode = Field(default=LanguageCode.EN, description="Target language")
    fallback_language: LanguageCode = Field(default=LanguageCode.EN, description="Fallback language")


class I18nProductData(BaseModel):
    """i18n product data structure."""
    name: I18nData
    description: I18nData
    short_description: Optional[I18nData] = None
    categories: List[Dict[str, Any]] = Field(default_factory=list)
    images: List[Dict[str, Any]] = Field(default_factory=list)
    attributes: List[Dict[str, Any]] = Field(default_factory=list)
    price: str
    type: str = "simple"
    stock_quantity: Optional[int] = None
    weight: Optional[str] = None


class I18nPostData(BaseModel):
    """i18n post data structure."""
    title: I18nData
    content: I18nData
    excerpt: Optional[I18nData] = None
    status: str = "draft"
    categories: List[int] = Field(default_factory=list)
    tags: List[int] = Field(default_factory=list)
    featured_media: Optional[int] = None
    meta: Dict[str, Any] = Field(default_factory=dict)


class I18nOrderData(BaseModel):
    """i18n order data structure."""
    payment_method: str = "bacs"
    payment_method_title: I18nData
    set_paid: bool = False
    billing: Dict[str, Any]
    shipping: Dict[str, Any]
    line_items: List[Dict[str, Any]] = Field(default_factory=list) 