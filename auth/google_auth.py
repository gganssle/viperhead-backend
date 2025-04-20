from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Verify Google OAuth token and return user info.
    
    Args:
        credentials: Bearer token from the Authorization header
        
    Returns:
        dict: User information from the verified token
        
    Raises:
        HTTPException: If token is invalid or verification fails
    """
    try:
        # Get the Google Client ID from environment
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        if not client_id:
            raise HTTPException(
                status_code=500,
                detail="Google Client ID not configured"
            )

        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            credentials.credentials, 
            requests.Request(), 
            client_id
        )

        # Verify issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid issuer.')
            
        return idinfo
        
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )
