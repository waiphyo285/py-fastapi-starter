from fastapi import Request
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status

from app.core.rate_limiter import limiter
from app.services.auth.jwt import create_token

router = APIRouter()
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/token", response_model=TokenResponse)
@limiter.limit("5/minute") # ⏱️ 5 requests per minute
async def login(request: Request, body: LoginRequest):
    # This is mocked. Replace with actual user DB check.
    if body.username != "admin" or body.password != "secret":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_token({"sub": body.username})
    return {"access_token": token, "token_type": "bearer"}