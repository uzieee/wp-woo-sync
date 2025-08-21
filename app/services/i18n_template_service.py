import os
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template
from app.models.i18n_schemas import I18nData, LanguageCode


class I18nTemplateService:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def extract_i18n_data(self, data: Dict[str, Any]) -> Dict[str, I18nData]:
        i18n_data = {}
        
        for key, value in data.items():
            if isinstance(value, dict) and any(lang in value for lang in ['en', 'fr', 'de', 'it', 'es']):
                i18n_data[key] = I18nData(**value)
            elif isinstance(value, str):
                i18n_data[key] = I18nData(
                    en={"translation": value, "notes": f"Auto-generated for {key}"}
                )
        
        return i18n_data
    
    def transform_to_wc_product_i18n(self, client_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
        i18n_data = self.extract_i18n_data(client_data)
        
        template_content = """
{
    "name": "{{ i18n_data.get('name', {}).get_translation(language) if i18n_data.get('name') else client_data.get('name', 'Product') }}",
    "type": "{{ client_data.get('type', 'simple') }}",
    "regular_price": "{{ client_data.get('price', client_data.get('regular_price', '0')) }}",
    "description": "{{ i18n_data.get('description', {}).get_translation(language) if i18n_data.get('description') else client_data.get('description', client_data.get('content', '')) }}",
    "short_description": "{{ i18n_data.get('short_description', {}).get_translation(language) if i18n_data.get('short_description') else client_data.get('short_description', client_data.get('summary', '')) }}",
    "categories": [
        {% for category in client_data.get('categories', []) %}
        {
            "id": {{ category.get('id', 0) }},
            "name": "{{ category.get('name', '') }}"
        }{% if not loop.last %},{% endif %}
        {% endfor %}
    ],
    "images": [
        {% for image in client_data.get('images', []) %}
        {
            "src": "{{ image.get('url', image.get('src', '')) }}",
            "name": "{{ image.get('name', image.get('alt', '')) }}"
        }{% if not loop.last %},{% endif %}
        {% endfor %}
    ],
    "attributes": [
        {% for attr in client_data.get('attributes', []) %}
        {
            "name": "{{ attr.get('name', '') }}",
            "visible": {{ attr.get('visible', true) | lower }},
            "variation": {{ attr.get('variation', false) | lower }},
            "options": [
                {% for option in attr.get('options', []) %}
                "{{ option }}"{% if not loop.last %},{% endif %}
                {% endfor %}
            ]
        }{% if not loop.last %},{% endif %}
        {% endfor %}
    ],
    "stock_quantity": {{ client_data.get('stock_quantity', client_data.get('stock', 0)) }},
    "weight": "{{ client_data.get('weight', '0') }}"
}
        """
        
        template = Template(template_content)
        rendered = template.render(
            client_data=client_data,
            i18n_data=i18n_data,
            language=language
        )
        
        import json
        return json.loads(rendered)
    
    def transform_to_wc_order_i18n(self, client_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
        i18n_data = self.extract_i18n_data(client_data)
        
        template_content = """
{
    "payment_method": "{{ client_data.get('payment_method', 'bacs') }}",
    "payment_method_title": "{{ i18n_data.get('payment_method_title', {}).get_translation(language) if i18n_data.get('payment_method_title') else client_data.get('payment_method_title', 'Bank transfer') }}",
    "set_paid": {{ client_data.get('set_paid', false) | lower }},
    "billing": {
        "first_name": "{{ client_data.get('billing', {}).get('first_name', client_data.get('customer', {}).get('first_name', '')) }}",
        "last_name": "{{ client_data.get('billing', {}).get('last_name', client_data.get('customer', {}).get('last_name', '')) }}",
        "address_1": "{{ client_data.get('billing', {}).get('address_1', '') }}",
        "address_2": "{{ client_data.get('billing', {}).get('address_2', '') }}",
        "city": "{{ client_data.get('billing', {}).get('city', '') }}",
        "state": "{{ client_data.get('billing', {}).get('state', '') }}",
        "postcode": "{{ client_data.get('billing', {}).get('postcode', '') }}",
        "country": "{{ client_data.get('billing', {}).get('country', '') }}",
        "email": "{{ client_data.get('billing', {}).get('email', client_data.get('customer', {}).get('email', '')) }}",
        "phone": "{{ client_data.get('billing', {}).get('phone', '') }}"
    },
    "shipping": {
        "first_name": "{{ client_data.get('shipping', {}).get('first_name', '') }}",
        "last_name": "{{ client_data.get('shipping', {}).get('last_name', '') }}",
        "address_1": "{{ client_data.get('shipping', {}).get('address_1', '') }}",
        "address_2": "{{ client_data.get('shipping', {}).get('address_2', '') }}",
        "city": "{{ client_data.get('shipping', {}).get('city', '') }}",
        "state": "{{ client_data.get('shipping', {}).get('state', '') }}",
        "postcode": "{{ client_data.get('shipping', {}).get('postcode', '') }}",
        "country": "{{ client_data.get('shipping', {}).get('country', '') }}"
    },
    "line_items": [
        {% for item in client_data.get('items', client_data.get('line_items', [])) %}
        {
            "product_id": {{ item.get('product_id', item.get('id', 0)) }},
            "quantity": {{ item.get('quantity', 1) }},
            "name": "{{ item.get('name', '') }}",
            "price": "{{ item.get('price', '0') }}"
        }{% if not loop.last %},{% endif %}
        {% endfor %}
    ]
}
        """
        
        template = Template(template_content)
        rendered = template.render(
            client_data=client_data,
            i18n_data=i18n_data,
            language=language
        )
        
        import json
        return json.loads(rendered)
    
    def transform_to_wp_post_i18n(self, client_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
        i18n_data = self.extract_i18n_data(client_data)
        
        template_content = """
{
    "title": "{{ i18n_data.get('title', {}).get_translation(language) if i18n_data.get('title') else client_data.get('title', client_data.get('name', 'Post')) }}",
    "content": "{{ i18n_data.get('content', {}).get_translation(language) if i18n_data.get('content') else client_data.get('content', client_data.get('description', '')) }}",
    "excerpt": "{{ i18n_data.get('excerpt', {}).get_translation(language) if i18n_data.get('excerpt') else client_data.get('excerpt', client_data.get('summary', client_data.get('short_description', ''))) }}",
    "status": "{{ client_data.get('status', 'publish') }}",
    "categories": [
        {% for category in client_data.get('categories', []) %}
        {{ category.get('id', 0) }}{% if not loop.last %},{% endif %}
        {% endfor %}
    ],
    "tags": [
        {% for tag in client_data.get('tags', []) %}
        {{ tag.get('id', 0) }}{% if not loop.last %},{% endif %}
        {% endfor %}
    ],
    "featured_media": {{ client_data.get('featured_media', client_data.get('image_id', 0)) }},
    "meta": {
        {% for key, value in client_data.get('meta', {}).items() %}
        "{{ key }}": "{{ value }}"{% if not loop.last %},{% endif %}
        {% endfor %}
    }
}
        """
        
        template = Template(template_content)
        rendered = template.render(
            client_data=client_data,
            i18n_data=i18n_data,
            language=language
        )
        
        import json
        return json.loads(rendered)


i18n_template_service = I18nTemplateService() 