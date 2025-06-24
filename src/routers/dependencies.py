import firebase_admin
from firebase_admin import credentials,auth
from fastapi import HTTPException,Depends,status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.adk.sessions import DatabaseSessionService
import os
import json
# Define the environment variable name where the JSON content will be stored.
# This MUST match the ENV_VAR_NAME in your entrypoint.sh script.
FIREBASE_CREDS_ENV_VAR = "FIREBASE_SERVICE_ACCOUNT_JSON"

# Load the JSON string from the environment variable
creds_json_string = os.environ.get(FIREBASE_CREDS_ENV_VAR)

# Check if the environment variable is missing
if not creds_json_string:
    raise RuntimeError(f"Missing Firebase credentials in environment variable: '{FIREBASE_CREDS_ENV_VAR}'. "
                       "Ensure your entrypoint.sh script is setting this variable correctly.")

# Initialize Firebase App
if not firebase_admin._apps:
    try:
        # Parse the JSON string into a Python dictionary
        creds_dict = json.loads(creds_json_string)
        
        # Initialize Firebase with the dictionary (not a file path)
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(credential=cred)
        print("Firebase Admin SDK initialized successfully from environment variable.") # Add a success log
    except json.JSONDecodeError as e:
        # Handle cases where the environment variable content is not valid JSON
        error_msg = f"Failed to parse Firebase credentials JSON from environment variable '{FIREBASE_CREDS_ENV_VAR}': {e}. " \
                    "Please ensure the content of your secret file is valid JSON."
        print(f"ERROR: {error_msg}")
        raise RuntimeError(error_msg)
    except Exception as e:
        # Catch any other exceptions during Firebase Admin SDK initialization
        error_msg = f"Firebase Admin SDK initialization failed: {e}"
        print(f"ERROR: {error_msg}")
        raise RuntimeError(error_msg)

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
