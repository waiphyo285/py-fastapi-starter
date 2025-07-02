
from fastapi import Request
from pydantic import BaseModel
from fastapi import APIRouter, status

from core.limiter import limiter
from app.services.auth.jwt import create_token
from app.utils.response import respond_ok, respond_error

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/auth/token", response_model=TokenResponse)
@limiter.limit("5/minute")  # ⏱️ 5 requests per minute
async def login(request: Request, body: LoginRequest):
    try:
        # This is mocked. Replace with actual user DB check.
        if body.username != "admin" or body.password != "secret":
            return respond_error("Invalid username or password", status_code=status.HTTP_401_UNAUTHORIZED)

        token = create_token({"sub": body.username})
        return respond_ok(token)
    except Exception as e:
        return respond_error(str(e), status_code=500)
