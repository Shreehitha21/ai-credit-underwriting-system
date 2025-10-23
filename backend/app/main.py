import os
import sys
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add the project root to the Python path to ensure robust imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# create_db_and_tables is no longer imported
from app.routers import users, applications, admin
from app.websockets import sio
from ml.model import train_and_save_model

# --- Main Application Setup ---
api_app = FastAPI(title="AI Credit Underwriting System")

os.makedirs("uploads", exist_ok=True)
os.makedirs("reports", exist_ok=True)
os.makedirs("models_trained", exist_ok=True)

# --- THIS IS THE FIX FOR THE CORS ERROR ---
origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "https://ai-credit-underwriting-system.onrender.com", # Your live frontend URL
]
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.on_event("startup")
def on_startup():
    """
    On server startup, pre-train the AI model.
    The database tables are now created in the build/start step.
    """
    train_and_save_model()

# Mount static file directories FIRST
api_app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
api_app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# Include the API routers
api_app.include_router(users.router, prefix="/api", tags=["Users"])
api_app.include_router(applications.router, prefix="/api", tags=["Applications"])
api_app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@api_app.get("/api/health")
def health_check():
    return {"status": "ok"}

app = socketio.ASGIApp(sio, other_asgi_app=api_app)

