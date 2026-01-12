"""
Configuration settings for the Todo Application backend.
"""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file


class Settings:
    """
    Application settings loaded from environment variables.
    """
    def __init__(self):
        # App settings
        self.APP_NAME = "Todo Application API"
        self.APP_VERSION = "1.0.0"

        # Server settings
        self.SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
        self.SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

        # API settings
        self.API_V1_STR = "/api/v1"

        # Database settings
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
        print(f"DEBUG: Using DATABASE_URL: {self.DATABASE_URL}")

        # Auth settings
        self.BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-here")

        # CORS settings
        self.ALLOWED_ORIGINS = [
            "https://new-hackathon-2-reusable-intelligen.vercel.app/"
            "http://localhost",
            "http://localhost:3000",  # Default Next.js port
            "http://127.0.0.1:3000",
            "http://localhost:8000",  # For API testing
            "http://127.0.0.1:8000",
        ]

        # Debug mode
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# Create a settings instance
settings = Settings()