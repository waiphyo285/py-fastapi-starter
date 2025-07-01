import openai

from core.config import config
from core.logger import logger

openai.api_key = config.openai_key

def await_chat_cli():
    logger.info("💬 ChatGPT CLI (type 'exit' to quit)\n")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("Bye!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response =  openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages)
            reply = response.choices[0].message.content.strip()
            print(f"GPT: {reply}")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"Error: {e}")
