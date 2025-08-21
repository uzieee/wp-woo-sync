import httpx
import base64
from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from app.core.config import settings
from app.models.schemas import PaginationParams


class WooCommerceService:
    def __init__(self):
        self.base_url = settings.BASE_URL.rstrip('/')
        self.consumer_key = settings.WC_CONSUMER_KEY
        self.consumer_secret = settings.WC_CONSUMER_SECRET
        
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/wp-json/wc/v3/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_detail = e.response.json() if e.response.content else {"message": str(e)}
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail={
                        "error": "WooCommerce API error",
                        "details": error_detail,
                        "status_code": e.response.status_code
                    }
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "WooCommerce API connection error",
                        "details": str(e)
                    }
                )
    
    async def get_products(self, pagination: PaginationParams) -> Dict[str, Any]:
        params = {
            "page": pagination.page,
            "per_page": pagination.per_page
        }
        
        response = await self._make_request("GET", "products", params=params)
        
        async with httpx.AsyncClient() as client:
            count_response = await client.head(
                f"{self.base_url}/wp-json/wc/v3/products",
                headers=self.headers,
                params={"per_page": 1}
            )
            total_products = int(count_response.headers.get("X-WP-Total", 0))
            total_pages = int(count_response.headers.get("X-WP-TotalPages", 0))
        
        normalized_products = []
        for product in response:
            normalized_products.append({
                "id": product.get("id"),
                "name": product.get("name"),
                "type": product.get("type"),
                "status": product.get("status"),
                "price": product.get("price"),
                "regular_price": product.get("regular_price"),
                "sale_price": product.get("sale_price"),
                "description": product.get("description"),
                "short_description": product.get("short_description"),
                "categories": [
                    {
                        "id": cat.get("id"),
                        "name": cat.get("name"),
                        "slug": cat.get("slug")
                    } for cat in product.get("categories", [])
                ],
                "images": [
                    {
                        "id": img.get("id"),
                        "src": img.get("src"),
                        "name": img.get("name"),
                        "alt": img.get("alt")
                    } for img in product.get("images", [])
                ],
                "attributes": [
                    {
                        "id": attr.get("id"),
                        "name": attr.get("name"),
                        "visible": attr.get("visible"),
                        "variation": attr.get("variation"),
                        "options": attr.get("options", [])
                    } for attr in product.get("attributes", [])
                ],
                "stock_quantity": product.get("stock_quantity"),
                "stock_status": product.get("stock_status"),
                "weight": product.get("weight"),
                "dimensions": product.get("dimensions"),
                "date_created": product.get("date_created"),
                "date_modified": product.get("date_modified")
            })
        
        return {
            "items": normalized_products,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": total_products,
                "pages": total_pages
            },
            "total": total_products,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": total_pages
        }
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self._make_request("POST", "products", data=product_data)
        
        return {
            "id": response.get("id"),
            "name": response.get("name"),
            "type": response.get("type"),
            "status": response.get("status"),
            "price": response.get("price"),
            "regular_price": response.get("regular_price"),
            "sale_price": response.get("sale_price"),
            "description": response.get("description"),
            "short_description": response.get("short_description"),
            "categories": [
                {
                    "id": cat.get("id"),
                    "name": cat.get("name"),
                    "slug": cat.get("slug")
                } for cat in response.get("categories", [])
            ],
            "images": [
                {
                    "id": img.get("id"),
                    "src": img.get("src"),
                    "name": img.get("name"),
                    "alt": img.get("alt")
                } for img in response.get("images", [])
            ],
            "link": response.get("permalink"),
            "date_created": response.get("date_created"),
            "date_modified": response.get("date_modified")
        }
    
    async def get_orders(self, pagination: PaginationParams) -> Dict[str, Any]:
        params = {
            "page": pagination.page,
            "per_page": pagination.per_page
        }
        
        response = await self._make_request("GET", "orders", params=params)
        
        async with httpx.AsyncClient() as client:
            count_response = await client.head(
                f"{self.base_url}/wp-json/wc/v3/orders",
                headers=self.headers,
                params={"per_page": 1}
            )
            total_orders = int(count_response.headers.get("X-WP-Total", 0))
            total_pages = int(count_response.headers.get("X-WP-TotalPages", 0))
        
        normalized_orders = []
        for order in response:
            normalized_orders.append({
                "id": order.get("id"),
                "number": order.get("number"),
                "status": order.get("status"),
                "currency": order.get("currency"),
                "total": order.get("total"),
                "subtotal": order.get("subtotal"),
                "total_tax": order.get("total_tax"),
                "shipping_total": order.get("shipping_total"),
                "payment_method": order.get("payment_method"),
                "payment_method_title": order.get("payment_method_title"),
                "billing": order.get("billing"),
                "shipping": order.get("shipping"),
                "line_items": [
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "product_id": item.get("product_id"),
                        "quantity": item.get("quantity"),
                        "price": item.get("price"),
                        "subtotal": item.get("subtotal"),
                        "total": item.get("total")
                    } for item in order.get("line_items", [])
                ],
                "date_created": order.get("date_created"),
                "date_modified": order.get("date_modified")
            })
        
        return {
            "items": normalized_orders,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": total_orders,
                "pages": total_pages
            },
            "total": total_orders,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": total_pages
        }
    
    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        response = await self._make_request("POST", "orders", data=order_data)
        
        return {
            "id": response.get("id"),
            "number": response.get("number"),
            "status": response.get("status"),
            "currency": response.get("currency"),
            "total": response.get("total"),
            "subtotal": response.get("subtotal"),
            "total_tax": response.get("total_tax"),
            "shipping_total": response.get("shipping_total"),
            "payment_method": response.get("payment_method"),
            "payment_method_title": response.get("payment_method_title"),
            "billing": response.get("billing"),
            "shipping": response.get("shipping"),
            "line_items": [
                {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "product_id": item.get("product_id"),
                    "quantity": item.get("quantity"),
                    "price": item.get("price"),
                    "subtotal": item.get("subtotal"),
                    "total": item.get("total")
                } for item in response.get("line_items", [])
            ],
            "link": response.get("permalink"),
            "date_created": response.get("date_created"),
            "date_modified": response.get("date_modified")
        }


woocommerce_service = WooCommerceService() 