#!/usr/bin/env python3
import requests
import argparse
from dotenv import load_dotenv
import os
from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Load environment variables
load_dotenv()

def get_google_token() -> str:
    """Get a Google OAuth ID token by authenticating with Google"""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    if not client_id:
        raise ValueError("GOOGLE_CLIENT_ID environment variable is not set")
    if not client_secret:
        raise ValueError("GOOGLE_CLIENT_SECRET environment variable is not set")

    # OAuth 2.0 scopes
    SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email']
    
    # Create the OAuth config
    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost:8090"],
            "javascript_origins": ["http://localhost:8090"]
        }
    }
    
    # Create flow instance
    flow = InstalledAppFlow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri="http://localhost:8090"
    )
    
    # Run the OAuth flow
    print("\nOpening browser for Google Sign-In...")
    creds = flow.run_local_server(port=8090)
    return creds.id_token

def test_root(api_url: str):
    """Test the root endpoint (no auth required)"""
    print("\nTesting root endpoint...")
    response = requests.get(api_url)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_generate_image(api_url: str, id_token: str):
    """Test the image generation endpoint (requires auth)"""
    print("\nTesting generate-image endpoint...")
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.post(f"{api_url}/generate-image", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Image URL: {result['image_url']}")
    else:
        print(f"Error: {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Test the Snake-headed Lab Generator API")
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--token",
        help="Google OAuth ID token (if not provided, will launch browser for sign-in)"
    )
    
    args = parser.parse_args()
    api_url = args.api_url.rstrip("/")
    
    # Get token if not provided
    id_token = args.token
    if not id_token:
        id_token = get_google_token()
        print("\nObtained ID token from Google Sign-In")
    
    # Test both endpoints
    test_root(api_url)
    test_generate_image(api_url, id_token)

if __name__ == "__main__":
    main()
