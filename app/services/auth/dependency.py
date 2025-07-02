from fastapi import HTTPException, Header, status
from app.services.auth.jwt import verify_token

def jwt_required(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization",
        )

    try:
        return verify_token(authorization.split(" ")[1])
    except Exception as e:
          raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )