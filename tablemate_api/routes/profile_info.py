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

@router.get("/me")
async def get_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get the currently authenticated user's details, including admin status.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "email": current_user["email"],
        "is_admin": current_user.get("is_admin", False)  # Return is_admin field
    }
