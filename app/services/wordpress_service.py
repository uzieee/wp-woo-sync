"""
WordPress REST API service using httpx for async operations.
"""
import httpx
import base64
from typing import Dict, Any, Optional, List
from fastapi import HTTPException
from app.core.config import settings
from app.models.schemas import PaginationParams


class WordPressService:
    """Service for WordPress REST API operations."""
    
    def __init__(self):
        """Initialize WordPress service with authentication."""
        self.base_url = settings.BASE_URL.rstrip('/')
        self.username = settings.WP_USERNAME
        self.password = settings.WP_APP_PASSWORD
        
        # Create Basic Auth header
        credentials = f"{self.username}:{self.password}"
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
        """
        Make HTTP request to WordPress REST API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            
        Returns:
            API response data
            
        Raises:
            HTTPException: If API request fails
        """
        url = f"{self.base_url}/wp-json/wp/v2/{endpoint}"
        
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
                        "error": "WordPress API error",
                        "details": error_detail,
                        "status_code": e.response.status_code
                    }
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "WordPress API connection error",
                        "details": str(e)
                    }
                )
    
    async def get_posts(self, pagination: PaginationParams) -> Dict[str, Any]:
        """
        Get WordPress posts with pagination.
        
        Args:
            pagination: Pagination parameters
            
        Returns:
            Normalized posts response
        """
        params = {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "_embed": "true"  # Include featured media and other embedded data
        }
        
        response = await self._make_request("GET", "posts", params=params)
        
        async with httpx.AsyncClient() as client:
            count_response = await client.head(
                f"{self.base_url}/wp-json/wp/v2/posts",
                headers=self.headers,
                params={"per_page": 1}
            )
            total_posts = int(count_response.headers.get("X-WP-Total", 0))
            total_pages = int(count_response.headers.get("X-WP-TotalPages", 0))
        
        normalized_posts = []
        for post in response:
            normalized_posts.append({
                "id": post.get("id"),
                "title": post.get("title", {}).get("rendered", ""),
                "content": post.get("content", {}).get("rendered", ""),
                "excerpt": post.get("excerpt", {}).get("rendered", ""),
                "status": post.get("status"),
                "date": post.get("date"),
                "modified": post.get("modified"),
                "slug": post.get("slug"),
                "categories": post.get("categories", []),
                "tags": post.get("tags", []),
                "featured_media": post.get("featured_media"),
                "featured_media_url": post.get("_embedded", {}).get("wp:featuredmedia", [{}])[0].get("source_url") if post.get("_embedded") else None
            })
        
        return {
            "items": normalized_posts,
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": total_posts,
                "pages": total_pages
            },
            "total": total_posts,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": total_pages
        }
    
    async def create_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new WordPress post.
        
        Args:
            post_data: Post data in WordPress format
            
        Returns:
            Created post data
        """
        response = await self._make_request("POST", "posts", data=post_data)
        
        return {
            "id": response.get("id"),
            "title": response.get("title", {}).get("rendered", ""),
            "content": response.get("content", {}).get("rendered", ""),
            "excerpt": response.get("excerpt", {}).get("rendered", ""),
            "status": response.get("status"),
            "date": response.get("date"),
            "slug": response.get("slug"),
            "link": response.get("link"),
            "categories": response.get("categories", []),
            "tags": response.get("tags", []),
            "featured_media": response.get("featured_media")
        }
    
    async def get_post(self, post_id: int) -> Dict[str, Any]:
        """
        Get a specific WordPress post by ID.
        
        Args:
            post_id: WordPress post ID
            
        Returns:
            Post data
        """
        response = await self._make_request("GET", f"posts/{post_id}")
        
        return {
            "id": response.get("id"),
            "title": response.get("title", {}).get("rendered", ""),
            "content": response.get("content", {}).get("rendered", ""),
            "excerpt": response.get("excerpt", {}).get("rendered", ""),
            "status": response.get("status"),
            "date": response.get("date"),
            "modified": response.get("modified"),
            "slug": response.get("slug"),
            "link": response.get("link"),
            "categories": response.get("categories", []),
            "tags": response.get("tags", []),
            "featured_media": response.get("featured_media")
        }


# Global WordPress service instance
wordpress_service = WordPressService() 