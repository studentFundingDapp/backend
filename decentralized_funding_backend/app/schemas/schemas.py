from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    wallet_address: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    wallet_address: Optional[str] = None

class ProjectCreate(BaseModel):
    title: str
    description: str
    target_amount: float
    wallet_address: str
    deadline: datetime
    category: str
    tags: List[str] = []

class DonationCreate(BaseModel):
    amount: float
    transaction_hash: str
    message: Optional[str] = None