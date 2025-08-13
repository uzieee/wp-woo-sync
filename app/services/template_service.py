"""
Jinja2 template service for transforming client JSON to platform-specific payloads.
"""
import os
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template
from app.core.config import settings


class TemplateService:
    """Service for processing Jinja2 templates."""
    
    def __init__(self):
        """Initialize template environment."""
        template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a Jinja2 template with the given context.
        
        Args:
            template_name: Name of the template file
            context: Data context for template rendering
            
        Returns:
            Rendered template string
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            raise ValueError(f"Template rendering failed: {str(e)}")
    
    def transform_to_wc_product(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform client data to WooCommerce product format.
        
        Args:
            client_data: Arbitrary client JSON data
            
        Returns:
            WooCommerce product payload
        """
        template_content = """
{
    "name": "{{ client_data.get('name', client_data.get('title', 'Product')) }}",
    "type": "{{ client_data.get('type', 'simple') }}",
    "regular_price": "{{ client_data.get('price', client_data.get('regular_price', '0')) }}",
    "description": "{{ client_data.get('description', client_data.get('content', '')) }}",
    "short_description": "{{ client_data.get('short_description', client_data.get('summary', '')) }}",
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
    ]
}
        """
        
        template = Template(template_content)
        rendered = template.render(client_data=client_data)
        
        import json
        return json.loads(rendered)
    
    def transform_to_wc_order(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform client data to WooCommerce order format.
        
        Args:
            client_data: Arbitrary client JSON data
            
        Returns:
            WooCommerce order payload
        """
        template_content = """
{
    "payment_method": "{{ client_data.get('payment_method', 'bacs') }}",
    "payment_method_title": "{{ client_data.get('payment_method_title', 'Bank transfer') }}",
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
        rendered = template.render(client_data=client_data)
        
        import json
        return json.loads(rendered)
    
    def transform_to_wp_post(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform client data to WordPress post format.
        
        Args:
            client_data: Arbitrary client JSON data
            
        Returns:
            WordPress post payload
        """
        template_content = """
{
    "title": "{{ client_data.get('title', client_data.get('name', 'Post')) }}",
    "content": "{{ client_data.get('content', client_data.get('description', '')) }}",
    "excerpt": "{{ client_data.get('excerpt', client_data.get('summary', client_data.get('short_description', ''))) }}",
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
        rendered = template.render(client_data=client_data)
        
        import json
        return json.loads(rendered)


# Global template service instance
template_service = TemplateService() 