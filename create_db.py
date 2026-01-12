import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.core.database import engine
from backend.models.database import Base
# Import all models to ensure they are registered with the Base
from backend.models.database import User, Task

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
