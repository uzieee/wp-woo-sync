"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.scheduler import scheduler
from app.api import wc, wp

load_dotenv()


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
    description="FastAPI microservice for WordPress and WooCommerce synchronization",
    version="1.0.0",
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


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "WP/WC Sync API",
        "version": "1.0.0",
        "endpoints": {
            "woocommerce": "/wc",
            "wordpress": "/wp"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 