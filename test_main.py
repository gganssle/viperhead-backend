import pytest
import httpx
from httpx import ASGITransport
from main import app, client

@pytest.fixture
async def test_client():
    """Create a test client fixture."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_root(test_client):
    """Test the root endpoint returns the correct message."""
    response = await test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Snake-headed Lab Generator API"}


@pytest.mark.asyncio
async def test_generate_image_success(test_client, monkeypatch):
    """Test successful image generation."""
    # Mock the OpenAI client response
    mock_response = type('Response', (), {
        'data': [type('ImageData', (), {'url': 'https://fake-image-url.com/image.png'})()]
    })()
    
    def mock_generate(*args, **kwargs):
        return mock_response
    monkeypatch.setattr(client.images, "generate", mock_generate)
    
    response = await test_client.post("/generate-image")
    assert response.status_code == 200
    assert response.json() == {"image_url": "https://fake-image-url.com/image.png"}


@pytest.mark.asyncio
async def test_generate_image_failure(test_client, monkeypatch):
    """Test image generation failure handling."""
    def mock_generate(*args, **kwargs):
        raise Exception("API Error")
    monkeypatch.setattr(client.images, "generate", mock_generate)
    
    response = await test_client.post("/generate-image")
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]
