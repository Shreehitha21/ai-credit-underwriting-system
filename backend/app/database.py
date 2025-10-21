from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

load_dotenv()

# This is the crucial change: It now looks for a DATABASE_URL environment variable.
# On Render, this will be your PostgreSQL connection string.
# If it's not found, it falls back to the local SQLite database for development.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Use 'echo=False' for cleaner production logs and handle PostgreSQL connections
if DATABASE_URL.startswith("postgres"):
    engine = create_engine(DATABASE_URL, echo=False)
else:
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

