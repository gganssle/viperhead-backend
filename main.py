from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
import os
from dotenv import load_dotenv
from config.prompt_manager import PromptManager
from auth.google_auth import verify_token

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
    return {"message": "Snake-headed Lab Generator API"}

@app.post("/generate-image")
async def generate_image(user_info: dict = Depends(verify_token)):
    """
    Generate an image of a snake-headed black lab.
    Requires a valid Google OAuth token in the Authorization header.
    
    Example:
        Authorization: Bearer <google_oauth_token>
    """
    try:
        # Log the authenticated user's email
        user_email = user_info.get('email')
        print(f"Generating image for user: {user_email}")
        
        prompt = prompt_manager.generate_prompt()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return {"image_url": response.data[0].url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
