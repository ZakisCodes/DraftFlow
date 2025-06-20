from fastapi import FastAPI, Request
from .routers import router as api_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from google.adk.sessions import DatabaseSessionService
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
load_dotenv()
DB_URL = "sqlite:///./multi_agent_data1.db"

# Create a lifespan event to initialize and clean up the session service
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Application starting up...")
    
    # Initialize the DatabaseSessionService instance and store it in app.state
    # This service will manage sessions in the specified SQLite database
    try:
        #app.state.session_service =DatabaseSessionService(
         #  db_url=DB_URL,
          # connect_args={"ssl": "require"})
        app.state.session_service =DatabaseSessionService(db_url=DB_URL)
        print("Database session service initialized successfully.")
    except Exception as e:
        print("Database session service initialized failed.")
        print(e)

    
    # Optional: You might want to ensure the database schema is created/upgraded here.
    # The DatabaseSessionService usually handles table creation on first access,
    # but explicit setup might be required for production.
    
    yield # This is where the application runs, handling requests

    # Shutdown code
    print("Application shutting down...")
    # For SQLite, explicit closing might not be necessary, but for other DBs,
    # you might close connections here if the session service provided a method for it.
    
app = FastAPI(
    title="DraftFlow",
    version="1.0.0",
    lifespan=lifespan,
    )

# middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend origin allow_origins=["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Custom Middleware to Add Headers
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
#    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    return response

@app.get("/api/firebase-config")
async def get_firebase_config():
    return {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGIN_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
    }

# loading the endpoints
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
