from fastapi import APIRouter, Depends, HTTPException
from tablemate_api.auth.dependencies import get_current_user  # Import your authentication dependency

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me/email")
async def get_user_email(current_user: dict = Depends(get_current_user)):
    """
    Get the currently authenticated user's email.
    """
    if not current_user or "email" not in current_user:
        raise HTTPException(status_code=401, detail="Could not retrieve user email")

    return {"email": current_user["email"]}
