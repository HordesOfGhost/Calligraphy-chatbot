import firebase_admin
from fastapi import Request, HTTPException
from firebase_admin import auth, credentials
from .config import firebase_config

cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

def verify_token(request: Request):
    """
    Verifies the Firebase ID token from the Authorization header in the request.

    Args:
        request (Request): The incoming HTTP request containing the Authorization header.

    Returns:
        dict: A dictionary containing the user's UID and optionally their email.

    Raises:
        HTTPException: 
            - 403 if the Authorization header is missing or malformed.
            - 401 if the token is invalid or verification fails.
    """

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Missing or invalid Authorization header")

    id_token = auth_header.split(" ")[1]

    try:
        decoded = auth.verify_id_token(id_token)
        return {"uid": decoded["uid"], "email": decoded.get("email")}
    except Exception as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")