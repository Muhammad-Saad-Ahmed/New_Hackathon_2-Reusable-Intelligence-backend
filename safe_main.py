"""
Safe FastAPI application for the Todo Application backend.
This version includes proper error handling and safe initialization.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv  # Make sure to install python-dotenv
import logging
import sys
import os

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the Python path to resolve imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    # Import after setting up path to avoid import-time errors
    from backend.api.v1.tasks import router as tasks_router
    from backend.api.v1.auth import router as auth_router
    from backend.core.config import settings
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Unexpected error during imports: {e}")
    sys.exit(1)


# Create the FastAPI app instance
try:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Todo Application API - Backend for the Todo Application",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        # Disable docs in production for security
        docs_url="/docs" if os.getenv("DEBUG", "False").lower() == "true" else None,
        redoc_url="/redoc" if os.getenv("DEBUG", "False").lower() == "true" else None,
    )
    logger.info("FastAPI app created successfully")
except Exception as e:
    logger.error(f"Failed to create FastAPI app: {e}")
    sys.exit(1)


# Add CORS middleware - this should be added after app creation
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware added successfully")
except Exception as e:
    logger.error(f"Failed to add CORS middleware: {e}")
    sys.exit(1)


# Include API routers - this should be done after app creation and middleware setup
try:
    app.include_router(tasks_router, prefix=settings.API_V1_STR, tags=["tasks"])
    app.include_router(auth_router, prefix=settings.API_V1_STR, tags=["auth"])
    logger.info("API routers included successfully")
except Exception as e:
    logger.error(f"Failed to include API routers: {e}")
    sys.exit(1)


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
    import uvicorn
    
    # Use 127.0.0.1 instead of 0.0.0.0 for Windows compatibility
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("SERVER_PORT", 8000))
    reload = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}, reload={reload}")
    
    try:
        uvicorn.run(
            "main:app",  # Use module:app format
            host=host,
            port=port,
            reload=reload,
            # Additional options for Windows compatibility
            workers=1,  # Use single worker for development
        )
    except Exception as e:
        logger.error(f"Failed to start uvicorn server: {e}")
        sys.exit(1)