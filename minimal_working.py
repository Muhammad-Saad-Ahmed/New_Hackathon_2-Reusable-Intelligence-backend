"""
Minimal working FastAPI application for the Todo Application backend.
This version avoids problematic dependencies for Python 3.14 compatibility.
"""
from fastapi import FastAPI
import uvicorn
import os


# Simple settings without pydantic
class Settings:
    def __init__(self):
        self.APP_NAME = "Todo Application API"
        self.APP_VERSION = "1.0.0"
        self.API_V1_STR = "/api/v1"
        self.SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
        self.SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        self.ALLOWED_ORIGINS = [
            "http://localhost",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]


settings = Settings()

# Create the FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Todo Application API - Backend for the Todo Application",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Todo Application API", "version": settings.APP_VERSION}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "Todo Application Backend"}


if __name__ == "__main__":
    uvicorn.run(
        "minimal_working:app",  # Use the module name where this code is defined
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )