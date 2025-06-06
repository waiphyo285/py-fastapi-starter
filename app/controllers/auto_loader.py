import os
import importlib

from pathlib import Path
from fastapi import APIRouter

def load_api_routers() -> list[tuple[str, APIRouter]]:
    routers = []
    api_path = Path(__file__).parent
    for file in os.listdir(api_path):
        if file.endswith("_api.py"):
            module_name = f"app.controllers.{file[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                prefix = f"/api/{file.replace('_api.py', '')}"
                routers.append((prefix, module.router))
    return routers
