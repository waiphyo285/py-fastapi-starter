import os
import importlib

from pathlib import Path
from fastapi import APIRouter

def load_routers() -> list[tuple[str, APIRouter]]:
    routers = []
    api_path = Path(__file__).parent
    for file in os.listdir(api_path):
        if file.endswith("_api.py"):
            module_name = f"app.controllers.{file[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                routers.append(('/api', module.router))
    print(f"Loaded {len(routers)} routers from {api_path}")
    return routers
