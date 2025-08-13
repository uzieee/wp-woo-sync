# WP/WC Sync API Documentation

## Overview

- WordPress REST API JSON formats (wp/v2)
- WooCommerce REST API JSON formats (wc/v3)
- Response structures from both platforms
- How our Jinja2 templates transform arbitrary client JSON

## WordPress REST API (wp/v2)

### POST /wp/v2/posts - Create Post

#### Accepted JSON Format
```json
{
  "title": "Post Title",
  "content": "Post content with HTML",
  "excerpt": "Short excerpt",
  "status": "publish",
  "categories": [1, 2, 3],
  "tags": [4, 5, 6],
  "featured_media": 123,
  "meta": {
    "custom_field": "value"
  }
}
```

#### Response Format
```json
{
  "id": 456,
  "date": "2024-01-15T10:30:00",
  "date_gmt": "2024-01-15T10:30:00",
  "guid": {
    "rendered": "https://eidcarosse.ch/?p=456"
  },
  "modified": "2024-01-15T10:30:00",
  "modified_gmt": "2024-01-15T10:30:00",
  "slug": "post-title",
  "status": "publish",
  "type": "post",
  "link": "https://eidcarosse.ch/post-title/",
  "title": {
    "rendered": "Post Title"
  },
  "content": {
    "rendered": "Post content with HTML",
    "protected": false
  },
  "excerpt": {
    "rendered": "Short excerpt",
    "protected": false
  },
  "author": 1,
  "featured_media": 123,
  "comment_status": "open",
  "ping_status": "open",
  "sticky": false,
  "template": "",
  "format": "standard",
  "meta": {
    "custom_field": "value"
  },
  "categories": [1, 2, 3],
  "tags": [4, 5, 6],
  "_links": {
    "self": [{"href": "https://eidcarosse.ch/wp-json/wp/v2/posts/456"}],
    "collection": [{"href": "https://eidcarosse.ch/wp-json/wp/v2/posts"}]
  }
}
```

### GET /wp/v2/posts - List Posts

#### Query Parameters
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)
- `_embed`: Include embedded data (true/false)

#### Response Format
```json
[
  {
    "id": 456,
    "date": "2024-01-15T10:30:00",
    "date_gmt": "2024-01-15T10:30:00",
    "guid": {
      "rendered": "https://example.com/?p=456"
    },
    "modified": "2024-01-15T10:30:00",
    "modified_gmt": "2024-01-15T10:30:00",
    "slug": "post-title",
    "status": "publish",
    "type": "post",
    "link": "https://eidcarosse.ch/post-title/",
    "title": {
      "rendered": "Post Title"
    },
    "content": {
      "rendered": "Post content with HTML",
      "protected": false
    },
    "excerpt": {
      "rendered": "Short excerpt",
      "protected": false
    },
    "author": 1,
    "featured_media": 123,
    "comment_status": "open",
    "ping_status": "open",
    "sticky": false,
    "template": "",
    "format": "standard",
    "meta": {},
    "categories": [1, 2, 3],
    "tags": [4, 5, 6],
    "_embedded": {
      "wp:featuredmedia": [
        {
          "id": 123,
          "date": "2024-01-15T10:30:00",
          "slug": "featured-image",
          "type": "attachment",
          "link": "https://eidcarosse.ch/featured-image/",
          "title": {
            "rendered": "Featured Image Title"
          },
          "source_url": "https://eidcarosse.ch/wp-content/uploads/featured-image.jpg"
        }
      ]
    }
  }
]
```

## WooCommerce REST API (wc/v3)

### POST /wc/v3/products - Create Product

#### Accepted JSON Format
```json
{
  "name": "Product Name",
  "type": "simple",
  "regular_price": "29.99",
  "sale_price": "24.99",
  "description": "Product description",
  "short_description": "Short product description",
  "categories": [
    {
      "id": 15,
      "name": "Electronics"
    }
  ],
  "images": [
    {
      "src": "https://eidcarosse.ch/wp-content/uploads/product-image.jpg",
      "name": "Product Image 1",
      "alt": "Product Image Alt Text"
    }
  ],
  "attributes": [
    {
      "name": "Color",
      "visible": true,
      "variation": true,
      "options": ["Red", "Blue", "Green"]
    }
  ],
  "stock_quantity": 100,
  "stock_status": "instock",
  "weight": "0.5",
  "dimensions": {
    "length": "10",
    "width": "5",
    "height": "2"
  }
}
```

#### Response Format
```json
{
  "id": 789,
  "name": "Product Name",
  "slug": "product-name",
  "permalink": "https://eidcarosse.ch/product/product-name/",
  "date_created": "2024-01-15T10:30:00",
  "date_created_gmt": "2024-01-15T10:30:00",
  "date_modified": "2024-01-15T10:30:00",
  "date_modified_gmt": "2024-01-15T10:30:00",
  "type": "simple",
  "status": "publish",
  "featured": false,
  "catalog_visibility": "visible",
  "description": "Product description",
  "short_description": "Short product description",
  "sku": "",
  "price": "24.99",
  "regular_price": "29.99",
  "sale_price": "24.99",
  "date_on_sale_from": null,
  "date_on_sale_from_gmt": null,
  "date_on_sale_to": null,
  "date_on_sale_to_gmt": null,
  "on_sale": true,
  "purchasable": true,
  "total_sales": 0,
  "virtual": false,
  "downloadable": false,
  "downloads": [],
  "download_limit": -1,
  "download_expiry": -1,
  "tax_status": "taxable",
  "tax_class": "",
  "manage_stock": false,
  "stock_quantity": 100,
  "stock_status": "instock",
  "backorders": "no",
  "backorders_allowed": false,
  "backordered": false,
  "sold_individually": false,
  "weight": "0.5",
  "dimensions": {
    "length": "10",
    "width": "5",
    "height": "2"
  },
  "shipping_required": true,
  "shipping_taxable": true,
  "shipping_class": "",
  "shipping_class_id": 0,
  "reviews_allowed": true,
  "average_rating": "0.00",
  "rating_count": 0,
  "images": [
    {
      "id": 456,
      "date_created": "2024-01-15T10:30:00",
      "date_created_gmt": "2024-01-15T10:30:00",
      "date_modified": "2024-01-15T10:30:00",
      "date_modified_gmt": "2024-01-15T10:30:00",
      "src": "https://eidcarosse.ch/wp-content/uploads/product-image.jpg",
      "name": "Product Image 1",
      "alt": "Product Image Alt Text"
    }
  ],
  "categories": [
    {
      "id": 15,
      "name": "Electronics",
      "slug": "electronics"
    }
  ],
  "tags": [],
  "attributes": [
    {
      "id": 0,
      "name": "Color",
      "position": 0,
      "visible": true,
      "variation": true,
      "options": ["Red", "Blue", "Green"]
    }
  ],
  "default_attributes": [],
  "variations": [],
  "grouped_products": [],
  "menu_order": 0,
  "meta_data": [],
  "_links": {
    "self": [{"href": "https://eidcarosse.ch/wp-json/wc/v3/products/789"}],
    "collection": [{"href": "https://eidcarosse.ch/wp-json/wc/v3/products"}]
  }
}
```

### GET /wc/v3/products - List Products

#### Query Parameters
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)

#### Response Format
```json
[
  {
    "id": 789,
    "name": "Product Name",
    "slug": "product-name",
    "permalink": "https://eidcarosse.ch/product/product-name/",
    "date_created": "2024-01-15T10:30:00",
    "date_created_gmt": "2024-01-15T10:30:00",
    "date_modified": "2024-01-15T10:30:00",
    "date_modified_gmt": "2024-01-15T10:30:00",
    "type": "simple",
    "status": "publish",
    "featured": false,
    "catalog_visibility": "visible",
    "description": "Product description",
    "short_description": "Short product description",
    "sku": "",
    "price": "24.99",
    "regular_price": "29.99",
    "sale_price": "24.99",
    "on_sale": true,
    "purchasable": true,
    "total_sales": 0,
    "virtual": false,
    "downloadable": false,
    "tax_status": "taxable",
    "tax_class": "",
    "manage_stock": false,
    "stock_quantity": 100,
    "stock_status": "instock",
    "backorders": "no",
    "backorders_allowed": false,
    "backordered": false,
    "sold_individually": false,
    "weight": "0.5",
    "dimensions": {
      "length": "10",
      "width": "5",
      "height": "2"
    },
    "shipping_required": true,
    "shipping_taxable": true,
    "shipping_class": "",
    "shipping_class_id": 0,
    "reviews_allowed": true,
    "average_rating": "0.00",
    "rating_count": 0,
    "images": [
      {
        "id": 456,
        "date_created": "2024-01-15T10:30:00",
        "date_created_gmt": "2024-01-15T10:30:00",
        "date_modified": "2024-01-15T10:30:00",
        "date_modified_gmt": "2024-01-15T10:30:00",
        "src": "https://eidcarosse.ch/wp-content/uploads/product-image.jpg",
        "name": "Product Image 1",
        "alt": "Product Image Alt Text"
      }
    ],
    "categories": [
      {
        "id": 15,
        "name": "Electronics",
        "slug": "electronics"
      }
    ],
    "tags": [],
    "attributes": [
      {
        "id": 0,
        "name": "Color",
        "position": 0,
        "visible": true,
        "variation": true,
        "options": ["Red", "Blue", "Green"]
      }
    ],
    "default_attributes": [],
    "variations": [],
    "grouped_products": [],
    "menu_order": 0,
    "meta_data": []
  }
]
```

### POST /wc/v3/orders - Create Order

#### Accepted JSON Format
```json
{
  "payment_method": "bacs",
  "payment_method_title": "Bank transfer",
  "set_paid": false,
  "billing": {
    "first_name": "Jean",
    "last_name": "Dupont",
    "address_1": "Avenue des Alpes 12",
    "address_2": "Bureau 3",
    "city": "Lausanne",
    "state": "VD",
    "postcode": "1001",
    "country": "CH",
    "email": "jean.dupont@email.ch",
    "phone": "+41 21 123 45 67"
  },
  "shipping": {
    "first_name": "Jean",
    "last_name": "Dupont",
    "address_1": "Avenue des Alpes 12",
    "address_2": "Bureau 3",
    "city": "Lausanne",
    "state": "VD",
    "postcode": "1001",
    "country": "CH"
  },
  "line_items": [
    {
      "product_id": 789,
      "quantity": 2,
      "name": "Product Name",
      "price": "24.99"
    }
  ]
}
```

#### Response Format
```json
{
  "id": 123,
  "number": "123",
  "order_key": "wc_order_abc123",
  "created_via": "rest-api",
  "version": "8.0.0",
  "status": "pending",
  "currency": "USD",
  "date_created": "2024-01-15T10:30:00",
  "date_created_gmt": "2024-01-15T10:30:00",
  "date_modified": "2024-01-15T10:30:00",
  "date_modified_gmt": "2024-01-15T10:30:00",
  "discount_total": "0.00",
  "discount_tax": "0.00",
  "shipping_total": "0.00",
  "shipping_tax": "0.00",
  "cart_tax": "0.00",
  "total": "49.98",
  "total_tax": "0.00",
  "prices_include_tax": false,
  "customer_id": 0,
  "customer_ip_address": "",
  "customer_user_agent": "",
  "customer_note": "",
      "billing": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "company": "",
      "address_1": "Avenue des Alpes 12",
      "address_2": "Bureau 3",
      "city": "Lausanne",
      "state": "VD",
      "postcode": "1001",
      "country": "CH",
      "email": "jean.dupont@email.ch",
      "phone": "+41 21 123 45 67"
    },
    "shipping": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "company": "",
      "address_1": "Avenue des Alpes 12",
      "address_2": "Bureau 3",
      "city": "Lausanne",
      "state": "VD",
      "postcode": "1001",
      "country": "CH"
    },
  "payment_method": "bacs",
  "payment_method_title": "Bank transfer",
  "transaction_id": "",
  "date_paid": null,
  "date_paid_gmt": null,
  "date_completed": null,
  "date_completed_gmt": null,
  "cart_hash": "",
  "meta_data": [],
  "line_items": [
    {
      "id": 456,
      "name": "Product Name",
      "product_id": 789,
      "variation_id": 0,
      "quantity": 2,
      "tax_class": "",
      "subtotal": "49.98",
      "subtotal_tax": "0.00",
      "total": "49.98",
      "total_tax": "0.00",
      "taxes": [],
      "meta_data": [],
      "sku": "",
      "price": 24.99
    }
  ],
  "tax_lines": [],
  "shipping_lines": [],
  "fee_lines": [],
  "coupon_lines": [],
  "refunds": [],
  "_links": {
    "self": [{"href": "https://example.com/wp-json/wc/v3/orders/123"}],
    "collection": [{"href": "https://example.com/wp-json/wc/v3/orders"}]
  }
}
```

### GET /wc/v3/orders - List Orders

#### Query Parameters
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10, max: 100)

#### Response Format
```json
[
  {
    "id": 123,
    "number": "123",
    "order_key": "wc_order_abc123",
    "created_via": "rest-api",
    "version": "8.0.0",
    "status": "pending",
    "currency": "USD",
    "date_created": "2024-01-15T10:30:00",
    "date_created_gmt": "2024-01-15T10:30:00",
    "date_modified": "2024-01-15T10:30:00",
    "date_modified_gmt": "2024-01-15T10:30:00",
    "discount_total": "0.00",
    "discount_tax": "0.00",
    "shipping_total": "0.00",
    "shipping_tax": "0.00",
    "cart_tax": "0.00",
    "total": "49.98",
    "total_tax": "0.00",
    "prices_include_tax": false,
    "customer_id": 0,
    "customer_ip_address": "",
    "customer_user_agent": "",
    "customer_note": "",
    "billing": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "company": "",
      "address_1": "Avenue des Alpes 12",
      "address_2": "Bureau 3",
      "city": "Lausanne",
      "state": "VD",
      "postcode": "1001",
      "country": "CH",
      "email": "jean.dupont@email.ch",
      "phone": "+41 21 123 45 67"
    },
    "shipping": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "company": "",
      "address_1": "Avenue des Alpes 12",
      "address_2": "Bureau 3",
      "city": "Lausanne",
      "state": "VD",
      "postcode": "1001",
      "country": "CH"
    },
    "payment_method": "bacs",
    "payment_method_title": "Bank transfer",
    "transaction_id": "",
    "date_paid": null,
    "date_paid_gmt": null,
    "date_completed": null,
    "date_completed_gmt": null,
    "cart_hash": "",
    "meta_data": [],
    "line_items": [
      {
        "id": 456,
        "name": "Product Name",
        "product_id": 789,
        "variation_id": 0,
        "quantity": 2,
        "tax_class": "",
        "subtotal": "49.98",
        "subtotal_tax": "0.00",
        "total": "49.98",
        "total_tax": "0.00",
        "taxes": [],
        "meta_data": [],
        "sku": "",
        "price": 24.99
      }
    ],
    "tax_lines": [],
    "shipping_lines": [],
    "fee_lines": [],
    "coupon_lines": [],
    "refunds": []
  }
]
```

## Template Transformation Examples

### Client JSON → WordPress Post

#### Input (Client JSON)
```json
{
  "title": "Nouveau Modèle BMW Série 3 2024",
  "content": "Découvrez le nouveau modèle BMW Série 3 2024 avec ses innovations technologiques et son design raffiné.",
  "summary": "Présentation du nouveau BMW Série 3 2024",
  "status": "draft",
  "categories": [
    {"id": 5, "name": "BMW"},
    {"id": 8, "name": "Nouveautés"}
  ],
  "tags": [
    {"id": 12, "name": "Série 3"},
    {"id": 15, "name": "2024"}
  ],
  "image_id": 234,
  "meta": {
    "author": "Marc Dubois",
    "read_time": "5 minutes"
  }
}
```

#### Transformed (WordPress Format)
```json
{
  "title": "Nouveau Modèle BMW Série 3 2024",
  "content": "Découvrez le nouveau modèle BMW Série 3 2024 avec ses innovations technologiques et son design raffiné.",
  "excerpt": "Présentation du nouveau BMW Série 3 2024",
  "status": "draft",
  "categories": [5, 8],
  "tags": [12, 15],
  "featured_media": 234,
  "meta": {
    "author": "Marc Dubois",
    "read_time": "5 minutes"
  }
}
```

### Client JSON → WooCommerce Product

#### Input (Client JSON)
```json
{
  "name": "BMW X5 xDrive40i 2024",
  "type": "simple",
  "price": "89,500",
  "description": "Le BMW X5 xDrive40i 2024 combine luxe, performance et technologie de pointe.",
  "summary": "SUV de luxe BMW X5 2024",
  "categories": [
    {"id": 15, "name": "BMW"},
    {"id": 22, "name": "SUV"}
  ],
  "images": [
    {"url": "https://eidcarosse.ch/wp-content/uploads/bmw-x5-front.jpg", "alt": "BMW X5 Vue Avant"},
    {"url": "https://eidcarosse.ch/wp-content/uploads/bmw-x5-side.jpg", "alt": "BMW X5 Vue Latérale"}
  ],
  "attributes": [
    {
      "name": "Couleur",
      "visible": true,
      "variation": true,
      "options": ["Alpine White", "Tanzanite Blue", "Carbon Black"]
    },
    {
      "name": "Intérieur",
      "visible": true,
      "variation": false,
      "options": ["Cuir Vernasca"]
    }
  ],
  "stock": 3,
  "weight": "2,150"
}
```

#### Transformed (WooCommerce Format)
```json
{
  "name": "BMW X5 xDrive40i 2024",
  "type": "simple",
  "regular_price": "89,500",
  "description": "Le BMW X5 xDrive40i 2024 combine luxe, performance et technologie de pointe.",
  "short_description": "SUV de luxe BMW X5 2024",
  "categories": [
    {"id": 15, "name": "BMW"},
    {"id": 22, "name": "SUV"}
  ],
  "images": [
    {"src": "https://eidcarosse.ch/wp-content/uploads/bmw-x5-front.jpg", "name": "BMW X5 Vue Avant", "alt": "BMW X5 Vue Avant"},
    {"src": "https://eidcarosse.ch/wp-content/uploads/bmw-x5-side.jpg", "name": "BMW X5 Vue Latérale", "alt": "BMW X5 Vue Latérale"}
  ],
  "attributes": [
    {
      "name": "Couleur",
      "visible": true,
      "variation": true,
      "options": ["Alpine White", "Tanzanite Blue", "Carbon Black"]
    },
    {
      "name": "Intérieur",
      "visible": true,
      "variation": false,
      "options": ["Cuir Vernasca"]
    }
  ],
  "stock_quantity": 3,
  "weight": "2,150"
}
```

### Client JSON → WooCommerce Order

#### Input (Client JSON)
```json
{
  "payment_method": "bank_transfer",
  "payment_method_title": "Virement Bancaire",
  "set_paid": false,
  "customer": {
    "first_name": "Pierre",
    "last_name": "Martin",
    "email": "pierre.martin@email.ch"
  },
  "billing": {
    "first_name": "Pierre",
    "last_name": "Martin",
    "address_1": "Rue du Rhône 45",
    "city": "Genève",
    "state": "GE",
    "postcode": "1204",
    "country": "CH",
    "email": "pierre.martin@email.ch",
    "phone": "+41 22 123 45 67"
  },
  "shipping": {
    "first_name": "Pierre",
    "last_name": "Martin",
    "address_1": "Rue du Rhône 45",
    "city": "Genève",
    "state": "GE",
    "postcode": "1204",
    "country": "CH"
  },
  "items": [
    {
      "product_id": 789,
      "quantity": 1,
      "name": "BMW X5 xDrive40i 2024",
      "price": "89,500"
    },
    {
      "product_id": 456,
      "quantity": 1,
      "name": "Pack Entretien BMW",
      "price": "2,500"
    }
  ]
}
```

#### Transformed (WooCommerce Format)
```json
{
  "payment_method": "bank_transfer",
  "payment_method_title": "Virement Bancaire",
  "set_paid": false,
  "billing": {
    "first_name": "Pierre",
    "last_name": "Martin",
    "address_1": "Rue du Rhône 45",
    "address_2": "",
    "city": "Genève",
    "state": "GE",
    "postcode": "1204",
    "country": "CH",
    "email": "pierre.martin@email.ch",
    "phone": "+41 22 123 45 67"
  },
  "shipping": {
    "first_name": "Pierre",
    "last_name": "Martin",
    "address_1": "Rue du Rhône 45",
    "address_2": "",
    "city": "Genève",
    "state": "GE",
    "postcode": "1204",
    "country": "CH"
  },
  "line_items": [
    {
      "product_id": 789,
      "quantity": 1,
      "name": "BMW X5 xDrive40i 2024",
      "price": "89,500"
    },
    {
      "product_id": 456,
      "quantity": 1,
      "name": "Pack Entretien BMW",
      "price": "2,500"
    }
  ]
}
```

## Field Mapping Reference

### WordPress Post Fields
| Client Field | WordPress Field | Notes |
|--------------|-----------------|-------|
| `title` | `title` | Direct mapping |
| `name` | `title` | Fallback for title |
| `content` | `content` | Direct mapping |
| `description` | `content` | Fallback for content |
| `excerpt` | `excerpt` | Direct mapping |
| `summary` | `excerpt` | Fallback for excerpt |
| `short_description` | `excerpt` | Fallback for excerpt |
| `status` | `status` | Direct mapping |
| `categories` | `categories` | Array of category IDs |
| `tags` | `tags` | Array of tag IDs |
| `featured_media` | `featured_media` | Direct mapping |
| `image_id` | `featured_media` | Fallback for featured_media |
| `meta` | `meta` | Direct mapping |

### WooCommerce Product Fields
| Client Field | WooCommerce Field | Notes |
|--------------|-------------------|-------|
| `name` | `name` | Direct mapping |
| `title` | `name` | Fallback for name |
| `type` | `type` | Direct mapping |
| `price` | `regular_price` | Direct mapping |
| `regular_price` | `regular_price` | Direct mapping |
| `description` | `description` | Direct mapping |
| `content` | `description` | Fallback for description |
| `short_description` | `short_description` | Direct mapping |
| `summary` | `short_description` | Fallback for short_description |
| `categories` | `categories` | Array of category objects |
| `images` | `images` | Array of image objects |
| `attributes` | `attributes` | Array of attribute objects |
| `stock` | `stock_quantity` | Direct mapping |
| `weight` | `weight` | Direct mapping |

### WooCommerce Order Fields
| Client Field | WooCommerce Field | Notes |
|--------------|-------------------|-------|
| `payment_method` | `payment_method` | Direct mapping |
| `payment_method_title` | `payment_method_title` | Direct mapping |
| `set_paid` | `set_paid` | Direct mapping |
| `billing` | `billing` | Direct mapping |
| `shipping` | `shipping` | Direct mapping |
| `items` | `line_items` | Fallback for line_items |
| `line_items` | `line_items` | Direct mapping |
| `customer.first_name` | `billing.first_name` | Nested mapping |
| `customer.last_name` | `billing.last_name` | Nested mapping |
| `customer.email` | `billing.email` | Nested mapping |

## Error Response Formats

### WordPress API Errors
```json
{
  "code": "rest_invalid_param",
  "message": "Invalid parameter(s): title",
  "data": {
    "status": 400,
    "params": {
      "title": "Title is required."
    }
  }
}
```

### WooCommerce API Errors
```json
{
  "code": "woocommerce_rest_product_invalid_id",
  "message": "Invalid product ID.",
  "data": {
    "status": 400
  }
}
```

### Our Normalized Error Response
```json
{
  "success": false,
  "error": "WordPress API error",
  "details": {
    "code": "rest_invalid_param",
    "message": "Invalid parameter(s): title",
    "status_code": 400
  }
}
``` 