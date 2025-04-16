
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.middlewares.watching_dog import WatchDogMiddleware

from app.api.mock_api import mock_router
from app.chat.open_ai import await_chat_cli

@asynccontextmanager
async def lifespan(app: FastAPI):
    await await_chat_cli()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(WatchDogMiddleware)

app.include_router(mock_router, prefix="/mock")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8001, reload=True)