from typing import Optional, Dict, Literal
from httpx import AsyncClient, Response, RequestError, HTTPStatusError

HttpMethod = Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

class HttpClient:
    def __init__(self, client: AsyncClient):
        self.client = client
        self.base_url = client.base_url

    async def _request(
        self,
        method: HttpMethod,
        endpoint: str,
        params: Optional[Dict[str, str]] = None,
        data: Optional[dict] = None
    ) -> Response:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = await self.client.request(
                method,
                url,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response
        except HTTPStatusError as e:
            print(f"HTTP status error occurred {url}: {e}")
            raise
        except RequestError as e:
            print(f"Request error occurred {url}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error occurred {url}: {e}")
            raise

    async def get(self, endpoint: str, params: Optional[Dict[str, str]] = None) -> Response:
        return await self._request('GET', endpoint, params=params)

    async def post(self, endpoint: str, data: dict) -> Response:
        return await self._request('POST', endpoint, data=data)

    async def put(self, endpoint: str, data: dict) -> Response:
        return await self._request('PUT', endpoint, data=data)

    async def patch(self, endpoint: str, data: dict) -> Response:
        return await self._request('PATCH', endpoint, data=data)

    async def delete(self, endpoint: str) -> Response:
        return await self._request('DELETE', endpoint)

    async def close(self):
        await self.client.aclose()