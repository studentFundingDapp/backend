from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..core.auth import (
    verify_password, 
    create_access_token, 
    get_password_hash,
    get_current_user,
    get_current_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..models.models import User, UserBase
from ..core.database import Database
from datetime import timedelta

router = APIRouter()

@router.post("/register")
async def signup(user: UserBase):
    db = Database.get_db()
    if await db["users"].find_one({"email": user.email}):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    user_dict = user.dict()
    user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
    user_dict["role"] = "user"  # Default role
    
    result = await db["users"].insert_one(user_dict)
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    return {"email": created_user["email"], "message": "User created successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = Database.get_db()
    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user