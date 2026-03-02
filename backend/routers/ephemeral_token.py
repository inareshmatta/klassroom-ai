import os
import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/api")
security = HTTPBearer(auto_error=False)


@router.post("/ephemeral-token")
async def mint_ephemeral_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Mint a short-lived scoped token for client-side Live API access.
    Client uses this token to open WebSocket to backend proxy.
    In production: validate Firebase JWT in credentials.credentials.
    """
    # TODO: Validate Firebase JWT token here in production
    # firebase_admin.auth.verify_id_token(credentials.credentials)

    try:
        from google.auth import default
        from google.auth.transport.requests import Request as GoogleRequest

        gcp_credentials, _ = default(
            scopes=["https://www.googleapis.com/auth/generative-language"]
        )
        gcp_credentials.refresh(GoogleRequest())

        return {
            "token": gcp_credentials.token,
            "expires_at": int(time.time()) + 60,
            "model": "gemini-2.5-flash-native-audio-preview-12-2025",
        }
    except Exception:
        # SECURITY: Never expose the raw API key to clients.
        # All Gemini calls go through the backend WebSocket proxy.
        raise HTTPException(
            status_code=503,
            detail="Ephemeral token service unavailable. Use the backend WebSocket proxy instead."
        )

