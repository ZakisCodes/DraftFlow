from fastapi import APIRouter, Depends
from .dependencies import get_current_user

router = APIRouter()

# Your existing /verify-token endpoint can stay, but it's not strictly necessary for security
# It's more of an informational endpoint for the client.
@router.get("/verify-token")
def verify_token_endpoint(decoded_token: dict = Depends(get_current_user)):
    """
    Endpoint to verify a Firebase ID Token.
    Returns the decoded token payload if valid, otherwise raises 401.
    This endpoint uses get_current_user as a dependency, so it's protected.
    """
    return {
        "status": "success",
        "uid": decoded_token.get("uid"),
        "email": decoded_token.get("email"),
        "name": decoded_token.get("name")
    }

# --- Example of a PROTECTED API Endpoint ---
# This is where the magic happens for your actual application logic
@router.get("/api/get_user_notes")
def get_user_notes(decoded_token: dict = Depends(get_current_user)):
    uid = decoded_token.get("uid")
    user_email = decoded_token.get("email")
    
    # NOW you can safely proceed to fetch notes for this 'uid' from your database
    # For example, using Firestore Admin SDK here or any other DB
    print(f"User {user_email} (UID: {uid}) is requesting notes.")
    
    # Simulate fetching notes from a database
    notes = [f"Note 1 for {user_email}", f"Note 2 for {user_email}"] 
    
    return {"status": "success", "user_uid": uid, "notes": notes}

# Add more protected endpoints as needed:
# @router.post("/api/create_document")
# def create_document(document_data: dict, decoded_token: dict = Depends(get_current_user)):
#     uid = decoded_token.get("uid")
#     # ... logic to save document for this uid ...
#     return {"message": "Document created", "user_uid": uid}