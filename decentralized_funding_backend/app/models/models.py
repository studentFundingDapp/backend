from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from bson import ObjectId
from enum import Enum

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not ObjectId.is_valid(v):
            raise ValueError('invalid ObjectId')
        return str(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema: dict[str, Any], field) -> dict[str, Any]:
        field_schema.update(type="string")
        return field_schema

class MongoBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class UserRole(str, Enum):
    ADMIN = "admin"
    DONOR = "donor"
    STUDENT = "student"

class ProjectStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class StudentProfile(MongoBaseModel):
    institution: str
    student_id: str
    field_of_study: str
    year_of_study: int
    is_verified: bool = False

class DonorProfile(MongoBaseModel):
    organization: Optional[str] = None
    preferred_categories: List[str] = []
    donation_history: List[str] = []
    total_donated: float = 0.0

class UserBase(MongoBaseModel):
    email: EmailStr
    password: str
    username: str
    role: UserRole = UserRole.STUDENT
    full_name: Optional[str] = None
    wallet_address: Optional[str] = None

class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    password_hash: str
    projects_created: List[PyObjectId] = []
    donations_made: List[PyObjectId] = []
    student_profile: Optional[StudentProfile] = None
    donor_profile: Optional[DonorProfile] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_verified: bool = False
    last_login: Optional[datetime] = None

class ProjectBase(MongoBaseModel):
    title: str
    description: str
    objectives: str
    deliverables: str
    category: str
    target_amount: float
    wallet_address: str
    deadline: datetime

class Project(ProjectBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    creator_id: PyObjectId
    current_amount: float = 0.0
    status: ProjectStatus = ProjectStatus.PENDING
    media_urls: List[str] = []
    donors: List[PyObjectId] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionBase(MongoBaseModel):
    amount: float
    transaction_hash: str
    message: Optional[str] = None
    asset_type: str = "XLM"

class Transaction(TransactionBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    donor_id: PyObjectId
    project_id: PyObjectId
    recipient_wallet: str
    status: str = "completed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    block_height: Optional[int] = None
    confirmed_at: Optional[datetime] = None