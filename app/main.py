import openai

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import config
from app.core.logger import logger
from app.middlewares.watching_dog import WatchDogMiddleware

from app.api.routes_mock import router_mock

openai.api_key = config.openai_key

async def await_chat_cli():
    logger.info("💬 ChatGPT CLI (type 'exit' to quit)\n")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("👋 Bye!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = await openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages)
            reply = response.choices[0].message.content.strip()
            print(f"🤖 GPT: {reply}")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"👻 Error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await await_chat_cli()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(WatchDogMiddleware)

app.include_router(router_mock, prefix="/mock")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8001, reload=True)