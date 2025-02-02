from fastapi import APIRouter, Depends
from tablemate_api.auth.dependencies import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome {current_user['email']}!"}
