from httpx import AsyncClient
from app.core.config import config

async def get_http_client(access_token: str = None) -> AsyncClient:
    base_url = config.mock_api_url
    headers = {
        "X-Custom-Header": "FastApi-Agent",
        "Authorization": f"Bearer {access_token}"
    }

    client = AsyncClient(base_url=base_url, headers=headers, timeout=10.0)
    return client
