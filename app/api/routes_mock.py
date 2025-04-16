from fastapi import APIRouter, Query, HTTPException, Depends
from httpx import AsyncClient, Request

from app.core.http import HttpClient
from app.core.http_client_mock import get_http_client

router_mock = APIRouter()

# Mapping function to map tag to API endpoint
def map_tag_to_api(tag: str) -> str:
    api_mapping = {
        "posts": "posts",
        "comments": "comments",
        "albums": "albums",
        "photos": "photos",
        "todos": "todos",
        "users": "users",
    }

    if tag not in api_mapping:
        raise HTTPException(status_code=404, detail="API service not found")

    return api_mapping[tag]

# Endpoint to map requests to external APIs
async def map_request(tag: str, params: dict = {}, data: dict = {}, method: str = "GET"):
    """
    This endpoint the request to a corresponding external API based on the `tag` query parameter.
    It dynamically handles different HTTP methods: GET, POST, PUT, DELETE.
    """

    # Map the tag to the corresponding external API
    api_endpoint = map_tag_to_api(tag)
    print(api_endpoint)

    # Create an HTTP client to make the request
    client = HttpClient(await get_http_client())

    try:
        if method.upper() == "GET":
            response = await client.get(api_endpoint, params=params)

        elif method.upper() == "POST":
            response = await client.post(api_endpoint, data=data)

        elif method.upper() == "PUT":
            response = await client.put(api_endpoint, data=data)

        elif method.upper() == "DELETE":
            response = await client.delete(api_endpoint, data=data)

        else:
            raise HTTPException(status_code=400, detail="Invalid HTTP method")

        # Return the response as JSON
        return response.json()

    except Exception as e:
        # Handle any exception that may arise during the request
        raise HTTPException(status_code=500, detail=f"Error in mapping the request: {str(e)}")


@router_mock.get("/test")
def home():
    return {"data": "Test from FastAPI!"}

@router_mock.get("/test_mapping")
async def test_mapping(tag: str = Query(..., description="Tag to map to an API")):
    # Call mapping function with the provided tag
    return await map_request(tag=tag)