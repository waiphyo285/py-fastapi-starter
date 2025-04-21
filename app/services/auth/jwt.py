from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.core.config import config

JWT_ALGO =  config.jwt_algo
JWT_SECRET = config.jwt_secrect
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
    except JWTError:
        return None
