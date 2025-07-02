from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta

from core.config import config
from app.utils.response import respond_error

JWT_ALGO =  config.jwt_algo
JWT_SECRET = config.jwt_secret
JWT_EXPIRES_MIN = config.jwt_expires_min

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=int(JWT_EXPIRES_MIN)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGO)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
