import os
import json

from dotenv import load_dotenv

load_dotenv()  # Load from .env file

class Configuration:
    debug: bool = os.getenv("DEBUG", "False") == "True"
    project_name: str = os.getenv("PROJECT_NAME", "FastAPI App")
    project_version: str = os.getenv("PROJECT_VERSION", "1.0.0")  
    mock_api_url: str = os.getenv("MOCK_API_URL", "https://jsonplaceholder.typicode.com")
    openai_key: str = os.getenv("OPENAI_KEY", "sk-proj-xxx")

config = Configuration()
