from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.scheduler import scheduler
from app.api import unified

load_dotenv()

templates = Jinja2Templates(directory="app/templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENABLE_SCHEDULER:
        scheduler.start()
    
    yield
    
    if settings.ENABLE_SCHEDULER:
        scheduler.shutdown()


app = FastAPI(
    title="WP/WC Sync API",
    description="WordPress and WooCommerce synchronization API",
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

app.include_router(unified.router, prefix="/api", tags=["Unified API"])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api")
async def api_info():
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
    return {"status": "healthy", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    ) 