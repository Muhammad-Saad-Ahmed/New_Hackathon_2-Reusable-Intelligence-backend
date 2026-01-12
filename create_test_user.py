
import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.config import settings
from backend.core.security import get_password_hash
from backend.models.database import User as UserModel, Base

def create_test_user():
    """
    Creates a test user in the database.
    """
    engine = create_engine(settings.DATABASE_URL)
    
    # Ensure tables are created (optional, but good for standalone scripts)
    Base.metadata.create_all(bind=engine)
    
    db = Session(bind=engine)

    try:
        # Check if user already exists
        existing_user = db.query(UserModel).filter(UserModel.email == "test@example.com").first()
        if existing_user:
            print("Test user 'test@example.com' already exists.")
            return

        # Create new user
        hashed_password = get_password_hash("testpass")
        db_user = UserModel(
            email="test@example.com",
            name="Test User",
            hashed_password=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"Successfully created user 'test@example.com' with ID: {db_user.id}")

    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
