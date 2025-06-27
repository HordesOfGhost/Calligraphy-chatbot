from fastapi import Request, HTTPException
from firebase_admin import auth

def verify_token(request: Request):
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