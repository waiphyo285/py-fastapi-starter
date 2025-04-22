from fastapi import APIRouter, Query, HTTPException, status

from app.core.http import HttpClient
from app.core.http_client_mock import get_http_client

router = APIRouter()

# Endpoint to map requests to external APIs
async def map_request(tag: str, params: dict = {}, data: dict = {}, method: str = "GET"):
    """
    This endpoint the request to a corresponding external API based on the `tag` query parameter.
    It dynamically handles different HTTP methods: GET, POST, PUT, DELETE.
    """

    # Create an HTTP client to make the request
    client = HttpClient(await get_http_client())

    try:
        if method.upper() == "GET":
            response = await client.get(tag, params=params)

        elif method.upper() == "POST":
            response = await client.post(tag, data=data)

        elif method.upper() == "PUT":
            response = await client.put(tag, data=data)

        elif method.upper() == "PATCH":
            response = await client.patch(tag, data=data)

        elif method.upper() == "DELETE":
            response = await client.delete(tag, data=data)

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid HTTP method")

        # Return the response as JSON
        return response.json()

    except Exception as e:
        # Handle any exception that may arise during the request
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"Error in mapping the request: {str(e)}")


@router.get("/test")
def home():
    return {"data": "Test from FastAPI!"}

@router.get("/test_mapping")
async def test_mapping(tag: str = Query(..., description="Tag to map to an API")):
    return await map_request(tag=tag)