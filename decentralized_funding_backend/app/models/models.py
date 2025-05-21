from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from bson import ObjectId
from enum import Enum

# Assuming you have these custom types and base model defined as you showed
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not v:
            return None
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema: dict[str, Any], field) -> dict[str, Any]:
        field_schema.update(type="string")
        return field_schema

    def __str__(self):
        return str(self)

class MongoBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

# Keep your existing Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    DONOR = "donor"
    STUDENT = "student"

class ProjectStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "cancelled" # Corrected from CANCELLED to COMPLETED based on typical flow
    CANCELLED = "cancelled"


# Keep StudentProfile and DonorProfile as they are

class StudentProfile(MongoBaseModel):
    institution: str
    student_id: str
    field_of_study: str
    year_of_study: int
    is_verified: bool = False # This could potentially be tied to account funding status

class DonorProfile(MongoBaseModel):
    organization: Optional[str] = None
    preferred_categories: List[str] = []
    donation_history: List[str] = []
    total_donated: float = 0.0


# Your UserBase model (input for registration - password will be hashed)
class UserBase(MongoBaseModel):
    email: EmailStr
    # password: str
    username: str
    full_name: Optional[str] = None
    # wallet_address will be generated, not provided by user at signup
    # role will be set by backend, not provided by user at signup


# Modified User model to include Stellar keys and link profiles
class User(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    password_hash: str # Stored hash of the password

    # --- Added fields for Stellar Keys ---
    stellar_public_key: Optional[str] = Field(default=None, alias="wallet_address") # Use wallet_address for public key
    stellar_secret_key_encrypted: Optional[str] = None # Store the ENCRYPTED secret key
    # ------------------------------------

    role: UserRole = UserRole.STUDENT # Set default role here

    projects_created: List[PyObjectId] = [] # List of Project ObjectIds created by this user (if student)
    donations_made: List[PyObjectId] = [] # List of Transaction ObjectIds made by this user (if donor)

    student_profile: Optional[StudentProfile] = None # Embedded student profile if role is STUDENT
    donor_profile: Optional[DonorProfile] = None # Embedded donor profile if role is DONOR

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Ensure correct aliases and config for MongoDB
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True, # Allows PyObjectId and Keypair types if needed directly in models (be careful)
        json_encoders={ObjectId: str}
    )
class UserPublic(UserBase):
    pass  # For external responses, no password
# Keep ProjectBase and Project models

class ProjectBase(MongoBaseModel):
    title: str
    description: str
    objectives: str
    deliverables: str
    category: str
    target_amount: float
    # wallet_address is now part of the User model, linked via creator_id
    # wallet_address: str # REMOVE THIS FIELD FROM ProjectBase

    deadline: datetime

class Project(ProjectBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    creator_id: PyObjectId # Link back to the User (student) who created the project

    current_amount: float = 0.0 # Keep track of funding received
    status: ProjectStatus = ProjectStatus.PENDING
    media_urls: List[str] = []
    # Donors who have contributed directly to this project (list of User ObjectIds)
    donors: List[PyObjectId] = []

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Keep TransactionBase and Transaction models

class TransactionBase(MongoBaseModel):
    amount: float
    transaction_hash: str # Stellar transaction hash
    message: Optional[str] = None # Memo field
    asset_type: str = "XLM" # e.g., "XLM", "USDC"
    # asset_issuer: Optional[str] = None # Add if using non-XLM assets


class Transaction(TransactionBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    # Link to the donor user (if direct donation) or null (if algorithmic)
    donor_id: Optional[PyObjectId] = None
    project_id: Optional[PyObjectId] = None # Link to the project being funded

    # Recipient is likely the student's public key or your central app key
    # recipient_wallet: str # This should be the destination_account_id from Stellar logic

    source_account_id: str # Stellar public key of the sender
    destination_account_id: str # Stellar public key of the receiver

    status: str = "completed" # Stellar transaction status ('successful', 'failed', etc.)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    block_height: Optional[int] = None # Ledger sequence number
    confirmed_at: Optional[datetime] = None # Timestamp when confirmed on ledger

    # Add fields for fees, operation type, etc if needed for detailed logging