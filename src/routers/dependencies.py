import firebase_admin
from firebase_admin import credentials,auth
from fastapi import HTTPException,Depends,status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.adk.sessions import DatabaseSessionService
import os

# Load from environment variable
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")

if not creds_json:
    raise RuntimeError("Missing Firebase credentials in environment variables.")
# initializing Firebase App
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(creds_json)
        firebase_admin.initialize_app(credential=cred)
    except Exception as e:
        # Log the error and raise an exception to prevent the app from starting if Firebase init fails
        print(f"ERROR: Failed to initialize Firebase Admin SDK: {e}")
        raise RuntimeError(f"Firebase Admin SDK initialization failed: {e}")


# --- Security Dependency for JWT Token Extraction ---
# This object will look for an "Authorization: Bearer <token>" header
security = HTTPBearer()

# --- Dependency to Get and Verify Current User ---
def get_current_user(credentials: HTTPAuthorizationCredentials=Depends(security)):
    """
    FastAPI dependency to get and verify the Firebase ID Token from the request's
    Authorization header.

    Args:
        credentials (HTTPAuthorizationCredentials): Automatically injected by FastAPI
                                                  from the 'Authorization: Bearer' header.

    Returns:
        dict: The decoded Firebase ID Token payload if valid.

    Raises:
        HTTPException: If the token is missing, malformed, or invalid/expired.
    """
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        print("Token Verification succesful")
        return decoded_token
    except Exception as e:
        print(f"Token Verification Failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
# You can add other utility dependencies here if needed
# For example:
# def get_firestore_db():
#     return firestore.client()

# --- DataBase Dependency for Agentic Sessions ---
def get_db_session_service(request: Request) -> DatabaseSessionService:
    """
    Dependency that provides the DatabaseSessionService instance from app.state.
    Includes error handling for robust service retrieval.
    """
    try:
        # Attempt to retrieve the session_service from app.state
        session_service = request.app.state.session_service
        
        # Optional: Add a check to ensure the retrieved object is of the expected type
        # if not isinstance(session_service, DatabaseSessionService):
        #     raise TypeError("session_service in app.state is not an instance of DatabaseSessionService")

        return session_service
    except AttributeError:
        # This occurs if 'session_service' is not found in 'request.app.state'
        print("Error: 'session_service' not found in app.state. Make sure it's initialized during app startup.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database session service not initialized on the server."
        )
    except Exception as e:
        # Catch any other unexpected errors during retrieval
        print(f"An unexpected error occurred while getting database session service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve database session service due to an unexpected error: {e}"
        )
