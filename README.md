# Viperhead Backend

A FastAPI service that generates images of snake-headed black labs using DALL-E 3.

## Setup

1. Create a Python virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Running the Server

Start the FastAPI server with:
```bash
uvicorn main:app --reload
```

The server will run at http://localhost:8000

## API Endpoints

### Root Endpoint
```bash
curl http://localhost:8000/
```

### Generate Snake-headed Lab Image
```bash
curl -X POST http://localhost:8000/generate-image
```

This will return a JSON response with the URL of the generated image:
```json
{
    "image_url": "https://..."
}
```
