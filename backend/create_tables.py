import os
import sys
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import time

# This ensures the script can find your 'app' module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # We must import all models here so that SQLModel's metadata
    # is aware of them BEFORE we call create_all()
    from app.models import User, CreditApplication
except ImportError as e:
    print(f"Error importing models: {e}")
    print("Please ensure your app/models.py file exists and is correct.")
    sys.exit(1)

def main():
    """
    Connects to the database and creates all tables.
    This is run during the build/start step to prevent race conditions.
    """
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("Error: DATABASE_URL is not set. Cannot create tables.")
        sys.exit(1)

    print("Connecting to database to create tables...")
    
    # Add a retry mechanism to give the database time to start
    retries = 5
    while retries > 0:
        try:
            engine = create_engine(DATABASE_URL, echo=True)
            SQLModel.metadata.create_all(engine)
            print("Database tables created successfully.")
            return # Success
        except Exception as e:
            print(f"Error creating database tables: {e}")
            retries -= 1
            print(f"Database might not be ready. Retrying in 5 seconds... ({retries} retries left)")
            time.sleep(5)
            
    print("Error: Could not create database tables after multiple retries.")
    sys.exit(1) # Exit with an error code to fail the build if this happens

if __name__ == "__main__":
    main()

