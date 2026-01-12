"""
Minimal working FastAPI application to test startup.
"""
from fastapi import FastAPI
import uvicorn


app = FastAPI(title="Minimal Todo Application API", version="1.0.0")


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Minimal Todo Application API", "status": "running"}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "Minimal Todo Application Backend"}


if __name__ == "__main__":
    # Run with uvicorn directly
    uvicorn.run(
        "minimal_main:app",
        host="127.0.0.1",  # Use 127.0.0.1 instead of 0.0.0.0 for Windows
        port=8000,
        reload=True,
        debug=True
    )