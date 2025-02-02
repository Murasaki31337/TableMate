from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import decode_access_token
from database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.users.find_one({"email": payload["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
