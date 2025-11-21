import os

from fastapi import Header, HTTPException

# Default demo key; override with ATLAS_API_KEY env var for real usage.
API_KEY = os.getenv("ATLAS_API_KEY", "atlas-demo-key")


def verify_api_key(x_api_key: str = Header(None)):
    """
    Simple API key guard. Configure the key via ATLAS_API_KEY env var.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
