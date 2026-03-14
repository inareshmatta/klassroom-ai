from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])

class AuthRequest(BaseModel):
    access_code: str

@router.post("/verify")
async def verify_access(req: AuthRequest):
    # Retrieve from environment variable - MUST be set in production
    VALID_CODE = os.getenv("JUDGE_ACCESS_CODE")
    
    if not VALID_CODE:
        # If not set, we shouldn't allow access by default for security
        raise HTTPException(status_code=500, detail="Server security configuration error")
    
    if req.access_code.strip().upper() == VALID_CODE.strip().upper():
        return {"status": "success", "message": "Access granted"}
    else:
        raise HTTPException(status_code=401, detail="Invalid access code")
