from fastapi import APIRouter, HTTPException
from database import db
from models import UserSignup, UserLogin
from auth.hashing import hash_password, verify_password
from auth.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
async def signup(user: UserSignup):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    user_data = {"email": user.email, "hashed_password": hashed_pw, "is_admin": user.is_admin}
    await db.users.insert_one(user_data)
    
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin):
    stored_user = await db.users.find_one({"email": user.email})
    if not stored_user or not verify_password(user.password, stored_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"email": user.email})
    return {"access_token": token, "token_type": "bearer"}
