"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.scheduler import scheduler
from app.api import wc, wp

load_dotenv()

# Setup templates
templates = Jinja2Templates(directory="app/templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENABLE_SCHEDULER:
        scheduler.start()
        print("Scheduler started")
    
    yield
    
    if settings.ENABLE_SCHEDULER:
        scheduler.shutdown()
        print("Scheduler shutdown")


app = FastAPI(
    title="WP/WC Sync API",
    description="FastAPI microservice for WordPress and WooCommerce synchronization with i18n support",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wc.router, prefix="/wc", tags=["WooCommerce"])
app.include_router(wp.router, prefix="/wp", tags=["WordPress"])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the frontend demo interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "message": "WP/WC Sync API v2.0.0",
        "version": "2.0.0",
        "features": [
            "i18n JSON Support",
            "Multi-language Transformation",
            "JSON Schema Validation",
            "WordPress Integration",
            "WooCommerce Integration"
        ],
        "endpoints": {
            "woocommerce": "/wc",
            "wordpress": "/wp",
            "frontend": "/"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 