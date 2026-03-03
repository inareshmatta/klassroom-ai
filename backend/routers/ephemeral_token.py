"""
Ephemeral Token Endpoint
========================
Mints a short-lived, single-use token for client-side Live API access.
The real API key NEVER leaves the backend.
"""
import os
import datetime
from fastapi import APIRouter
from services.gemini_client import get_client

router = APIRouter(prefix="/api")

LIVE_MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"


@router.post("/ephemeral-token")
async def mint_ephemeral_token():
    """
    Mint a short-lived, single-use ephemeral token for direct client-side
    Live API connection. The API key stays server-side.
    """
    client = get_client()
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    token = client.auth_tokens.create(
        config={
            "uses": 1,
            "expire_time": now + datetime.timedelta(minutes=30),
            "new_session_expire_time": now + datetime.timedelta(minutes=2),
            "http_options": {"api_version": "v1alpha"},
        }
    )

    return {
        "token": token.name,
        "model": LIVE_MODEL,
        "expires_at": int((now + datetime.timedelta(minutes=30)).timestamp()),
    }
