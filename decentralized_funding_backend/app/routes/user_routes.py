from fastapi import APIRouter, HTTPException, Depends
from ..models.models import User
from ..schemas.schemas import UserCreate, UserResponse
from ..core.database import Database

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    db = Database.get_db()
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.dict()
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return UserResponse(**created_user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    db = Database.get_db()
    if (user := await db.users.find_one({"_id": user_id})) is not None:
        return user
    raise HTTPException(status_code=404, detail="User not found")