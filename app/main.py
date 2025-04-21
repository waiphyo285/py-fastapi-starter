
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.middlewares.watching_dog import WatchDogMiddleware

from app.chat.open_ai import await_chat_cli

from app.api.mock_api import mock_router
from app.api.auth_api import auth_router
from app.api.book_api import book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await await_chat_cli()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(WatchDogMiddleware)

app.include_router(mock_router, prefix="/mock")
app.include_router(auth_router, prefix="/auth")
app.include_router(book_router, prefix="/books")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=9001, reload=True)