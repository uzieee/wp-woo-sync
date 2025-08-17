# WP/WC Sync (FastAPI + Jinja + i18n)

A FastAPI microservice that accepts arbitrary client JSON with i18n support, transforms it via Jinja templates into valid WordPress (wp/v2) and WooCommerce (wc/v3) payloads, pushes them to each platform, and also pulls data and normalizes responses for clients.

## 🚀 Features

- **i18n JSON Support**: Multi-language content using [Lokalise i18n format](https://lokalise.com/blog/json-l10n/#I18n_JSON_file_example)
- **Multi-language Transformation**: Automatic language selection with fallback to English
- **JSON Schema Validation**: Comprehensive validation for incoming and outgoing data
- **WordPress Integration**: Full CRUD operations for posts via wp/v2 REST API
- **WooCommerce Integration**: Product and order management via wc/v3 REST API
- **Authentication**: Application Passwords for WordPress, Consumer Keys for WooCommerce
- **Response Normalization**: Consistent, concise JSON responses for clients
- **Error Handling**: Graceful error surfacing with platform-specific error details
- **Pagination**: Support for page and per_page parameters
- **Scheduling**: Optional background sync with APScheduler
- **Frontend Demo**: Interactive web interface for testing and demonstration

## 🛠️ Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill values from client
bash run.sh
```

## 🌐 Frontend Demo

Visit `http://localhost:8000` to access the interactive demo interface where you can:

- Test i18n JSON transformations
- Switch between languages (EN, FR, DE, IT, ES)
- See real-time transformation results
- Test actual API endpoints
- View comprehensive examples

## 📝 i18n JSON Format

The system supports the [Lokalise i18n JSON format](https://lokalise.com/blog/json-l10n/#I18n_JSON_file_example):

```json
{
  "name": {
    "en": {
      "translation": "BMW X5 xDrive40i 2024",
      "notes": "Product name in English",
      "context": "Main product title",
      "limit": 50
    },
    "fr": {
      "translation": "BMW X5 xDrive40i 2024",
      "notes": "Nom du produit en français",
      "context": "Titre principal du produit",
      "limit": 50
    }
  }
}
```

## 🔌 API Endpoints

### WooCommerce
- `GET /wc/products` - List products with pagination
- `POST /wc/products` - Create product from i18n JSON
- `GET /wc/orders` - List orders with pagination  
- `POST /wc/orders` - Create order from i18n JSON

### WordPress
- `GET /wp/posts` - List posts with pagination
- `POST /wp/posts` - Create post from i18n JSON

### Demo & Info
- `GET /` - Interactive frontend demo
- `GET /api` - API information
- `GET /health` - Health check

## 🔧 Environment Variables

Copy `.env.example` to `.env` and configure:

- `BASE_URL`: Your WordPress/WooCommerce site URL
- `WP_USERNAME`: WordPress username
- `WP_APP_PASSWORD`: WordPress application password
- `WC_CONSUMER_KEY`: WooCommerce consumer key
- `WC_CONSUMER_SECRET`: WooCommerce consumer secret

## 🐳 Docker

```bash
docker build -t wp-wc-sync .
docker run -p 8000:8000 wp-wc-sync
```

## 📚 Documentation

See `API_DOCUMENTATION.md` for comprehensive API documentation including:
- Complete JSON schemas for WordPress and WooCommerce
- i18n transformation examples
- Field mapping reference
- Error response formats

## 🎯 Supported Languages

- English (en) - Default fallback
- French (fr)
- German (de)
- Italian (it)
- Spanish (es)

## 📋 Sample Files

- `samples/i18n_product_example.json` - Complete i18n product example
- See frontend demo for more examples
