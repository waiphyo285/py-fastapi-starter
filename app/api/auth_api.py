from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth.jwt import create_token

auth_router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@auth_router.post("/token", response_model=TokenResponse)
def login(request: LoginRequest):
    # This is mocked. Replace with actual user DB check.
    if request.username != "admin" or request.password != "secret":
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}