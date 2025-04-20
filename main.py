from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    The image will be a photorealistic black labrador retriever with its head 
    replaced by a realistic snake head, maintaining the lab's body posture 
    and proportions.

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
        response = client.images.generate(
            model="dall-e-3",
            prompt="A photorealistic black labrador retriever with its head replaced by a realistic snake head, maintaining the lab's body posture and proportions. The snake head should be seamlessly integrated, creating a surreal but cohesive hybrid creature.",
            n=1,
            size="1024x1024",
            quality="standard"
        )
        
        return JSONResponse(content={
            "image_url": response.data[0].url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
