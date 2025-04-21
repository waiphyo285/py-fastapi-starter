from fastapi import Header, HTTPException, status
from app.services.auth.jwt import verify_token

def jwt_required(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    
    token = authorization.split(" ")[1]
    return verify_token(token)
