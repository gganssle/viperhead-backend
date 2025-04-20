from typing import Optional
from pydantic import BaseModel

class OAuthConfig:
    """Google OAuth configuration."""
    GOOGLE_CLIENT_ID = None  # Set from environment variable
    GOOGLE_CLIENT_SECRET = None  # Set from environment variable
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_SCOPES = [
        "openid",
        "email",
        "profile"
    ]

class UserProfile(BaseModel):
    """User profile information from Google."""
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    email_verified: bool = False
