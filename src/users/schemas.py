import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from src.users.validators import Role, Belt

#TODO: Add model_config for each

class Input_forPublic_UserCreateSchema(BaseModel):
    # Mandatory user fields
    username: str = Field(min_length=5, max_length=30, description="The username of the user.")
    email: str = Field(min_length=10, max_length=40, description="The email address of the user.")
    password: str = Field(min_length=6, max_length=50, description="The user's password.")
    role: Role = Role.Student

    # Optional user fields
    height: Optional[int] = Field(default=None, ge=75, le=300, description="User's height in cm (75-300cm).")
    weight: Optional[int] = Field(default=None, ge=50, le=300, description="User's weight in kg (50-300kg).")
    birthdate: Optional[datetime] = None
    belt: Belt = Belt.White

    # Optional coach fields
    expertise: Optional[List[str]] = Field(default_factory=lambda: [""])
    affiliations: Optional[List[str]] = Field(default_factory=lambda: [""])
    coach_bio: Optional[str] = None
    price: Optional[int] = Field(default=None, ge=5, le=99, description="Coach price per session (5-99).")

    # Optional student fields
    areas_working_on: Optional[List[str]] = Field(default_factory=lambda: [""])

    #TODO: Add a model_config


class Response_forSelf_UserSchema(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime
    height: Optional[int] = None
    weight: Optional[int] = None
    birthdate: Optional[datetime] = None
    belt: str

    class Config:
        from_attributes = True
        use_enum_values = True

class Response_forSelf_ProfileSchema(Response_forSelf_UserSchema):
    pass


class Input_forSelf_CoachCreateModel(BaseModel):
    expertise: Optional[List[str]] = None
    affiliations: Optional[List[str]] = None
    coach_bio: Optional[str] = None
    price: Optional[int] = Field(
        default=None,
        ge=5,
        le=99,
        nullable=True
    )    

    #TODO: Add a model_config

class Response_forPublic_CoachProfile(BaseModel):
    username: str
    expertise: Optional[List[str]]
    affiliation: Optional[List[str]]
    coach_bio: Optional[str]

    class Config:
        from_attributes = True

class Response_forAccountHolder_CoachProfile(Response_forPublic_CoachProfile):
    price: int
    accepting_responses: bool

class Response_forSelf_CoachProfile(Response_forAccountHolder_CoachProfile):
    settings: str = "<Some user specific settings e.g., settings>"













# Will be deprecated soon

class StudentCreateModel(BaseModel): # ! This will change soon
    areas_working_on: Optional[List[str]] = None  # Optional field to describe areas the student is working on

    class Config:
        json_schema_extra = {
            "example": {
                "areas_working_on": "Guard Passing, Sweeps"
            }
        }


class StudentModel(BaseModel): # ! This will change soon
    student_id: uuid.UUID
    user_id: uuid.UUID  # Foreign key to User
    areas_working_on: Optional[List[str]]  # E.g., 'Guard Passing, Sweeps'

    class Config:
        from_attributes = True


class UserUpdateModel(BaseModel): # ! Will be going soon. Split out each field for fact tables
    username: Optional[str] = None
    role: Optional[Role] = None        