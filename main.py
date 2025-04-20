from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
import os
from dotenv import load_dotenv
from config.prompt_manager import PromptManager

# Load environment variables
load_dotenv()

# Initialize OpenAI client and prompt manager
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
prompt_manager = PromptManager()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Get API status and welcome message.

    Returns:
        dict: A dictionary containing a welcome message
            {
                "message": str
            }
    """
    return {"message": "Snake-headed Lab Generator API"}

@app.post("/generate-image")
async def generate_image():
    """Generate an image of a snake-headed black lab using DALL-E 3.

    Returns:
        JSONResponse: A JSON response containing the URL of the generated image
            {
                "image_url": str
            }

    Raises:
        HTTPException: If there's an error during image generation
            - status_code: 500
            - detail: Error message from the OpenAI API
    """
    try:
        # Generate the prompt using the prompt manager
        prompt = prompt_manager.generate_prompt()
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        
        return JSONResponse(content={
            "image_url": response.data[0].url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
