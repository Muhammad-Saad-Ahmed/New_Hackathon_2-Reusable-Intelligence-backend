"""
Database connection and session management for the Todo Application backend.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    # For PostgreSQL with Neon, we might need specific options
    pool_pre_ping=True,
    # Additional options can be added as needed
)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session for FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()