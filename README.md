# WP/WC Sync API

WordPress and WooCommerce synchronization API with i18n support.

## Features

- WordPress REST API integration
- WooCommerce REST API integration
- Multi-language (i18n) JSON support
- JSON schema validation
- Template-based data transformation
- Unified API endpoints

## Quick Start

### Prerequisites

- Python 3.11+
- WordPress site with REST API enabled
- WooCommerce with REST API enabled

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd wp-woo-sync
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp env.example .env
```

Edit `.env` with your configuration:
```env
# WordPress Configuration
BASE_URL=https://your-wordpress-site.com
WP_USERNAME=your_username
WP_APP_PASSWORD=your_application_password
WP_AUTH_TYPE=basic

# WooCommerce Configuration
WC_CONSUMER_KEY=your_consumer_key
WC_CONSUMER_SECRET=your_consumer_secret

# Application Configuration
ENABLE_SCHEDULER=false
SYNC_CRON=*/15 * * * *

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

4. Run the application:
```bash
./run.sh
```

Or with Docker:
```bash
docker build -t wp-woo-sync .
docker run -p 8000:8000 wp-woo-sync
```

## API Endpoints

### Unified API

- `POST /api/sync` - Unified endpoint for all operations

### Health Check

- `GET /health` - Health check endpoint
- `GET /api` - API information

### Frontend

- `GET /` - Web interface

## Usage Examples

### Create WooCommerce Product

```bash
curl -X POST "http://localhost:8000/api/sync" \
  -H "Content-Type: application/json" \
  -d '{
    "action_id": "create_wc_product",
    "data": {
      "name": {
        "en": {"translation": "Product Name", "notes": "Product name"},
        "fr": {"translation": "Nom du Produit", "notes": "Nom du produit"}
      },
      "description": {
        "en": {"translation": "Product description", "notes": "Product description"},
        "fr": {"translation": "Description du produit", "notes": "Description du produit"}
      },
      "price": "29.99",
      "type": "simple"
    },
    "language": "en"
  }'
```

### Create WordPress Post

```bash
curl -X POST "http://localhost:8000/api/sync" \
  -H "Content-Type: application/json" \
  -d '{
    "action_id": "create_wp_post",
    "data": {
      "title": {
        "en": {"translation": "Post Title", "notes": "Post title"},
        "fr": {"translation": "Titre de l\'article", "notes": "Titre de l\'article"}
      },
      "content": {
        "en": {"translation": "Post content", "notes": "Post content"},
        "fr": {"translation": "Contenu de l\'article", "notes": "Contenu de l\'article"}
      },
      "status": "publish"
    },
    "language": "en"
  }'
```

## Configuration

### WordPress Setup

1. Enable REST API in WordPress
2. Create an Application Password for API access
3. Configure `WP_USERNAME` and `WP_APP_PASSWORD` in `.env`

### WooCommerce Setup

1. Enable REST API in WooCommerce
2. Generate API keys (Consumer Key and Consumer Secret)
3. Configure `WC_CONSUMER_KEY` and `WC_CONSUMER_SECRET` in `.env`

## Development

### Running in Development Mode

Set `DEBUG=true` in your `.env` file to enable auto-reload.

### Testing

The API includes validation endpoints for testing:

- `POST /api/validate-product` - Validate product schema
- `POST /api/validate-i18n` - Validate i18n structure

## License

This project is licensed under the MIT License.
