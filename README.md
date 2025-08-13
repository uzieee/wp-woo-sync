# WP/WC Sync (FastAPI + Jinja)

A FastAPI microservice that accepts arbitrary client JSON, transforms it via Jinja templates into valid WordPress (wp/v2) and WooCommerce (wc/v3) payloads, pushes to those platforms, and pulls/normalizes responses for clients.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill values from client
bash run.sh
```

## Features

- **Flexible JSON Processing**: Accepts arbitrary client JSON and transforms via Jinja templates
- **WordPress Integration**: Full CRUD operations for posts via wp/v2 REST API
- **WooCommerce Integration**: Product and order management via wc/v3 REST API
- **Authentication**: Application Passwords for WordPress, Consumer Keys for WooCommerce
- **Response Normalization**: Consistent, concise JSON responses for clients
- **Error Handling**: Graceful error surfacing with platform-specific error details
- **Pagination**: Support for page and per_page parameters
- **Scheduling**: Optional background sync with APScheduler

## API Endpoints

### WooCommerce
- `GET /wc/products` - List products with pagination
- `POST /wc/products` - Create product from client JSON
- `GET /wc/orders` - List orders with pagination  
- `POST /wc/orders` - Create order from client JSON

### WordPress
- `GET /wp/posts` - List posts with pagination
- `POST /wp/posts` - Create post from client JSON

## Environment Variables

Copy `.env.example` to `.env` and configure:

- `BASE_URL`: Your WordPress/WooCommerce site URL
- `WP_USERNAME`: WordPress username
- `WP_APP_PASSWORD`: WordPress application password
- `WC_CONSUMER_KEY`: WooCommerce consumer key
- `WC_CONSUMER_SECRET`: WooCommerce consumer secret

## Docker

```bash
docker build -t wp-wc-sync .
docker run -p 8000:8000 wp-wc-sync
```
