import firebase_admin
from firebase_admin import credentials,auth
from fastapi import HTTPException,Depends,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# initializing Firebase App
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('/workspace/draftflow-b7b11-firebase-adminsdk-fbsvc-77f9fcd8a6.json')
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

