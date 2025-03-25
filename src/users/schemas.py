import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from src.users.validators import Role, Belt


class Input_forPublic_UserCreateSchema(BaseModel):
    username: str = Field(max_length=30)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    role: Role = Role.Student
    height: Optional[int] = None  # Optional height
    weight: Optional[int] = None  # Optional weight
    birthdate: Optional[datetime] = None  # Optional birthdate
    belt: Belt

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
                "role": "Student",
                "height": 180,
                "weight": 75,
                "birthdate": "1990-01-01T00:00:00",
            }
        }
    }

class UserUpdateModel(BaseModel): # ! Will be going soon. Split out each field for fact tables
    username: Optional[str] = None
    role: Optional[Role] = None


class Response_forSelf_UserSchema(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime
    height: Optional[int] = None  # Allow None for height
    weight: Optional[int] = None  # Allow None for weight
    birthdate: Optional[datetime] = None  # Allow None for birthdate
    belt: str

    class Config:
        from_attributes = True
        use_enum_values = True


class Input_forSelf_CoachCreateModel(BaseModel):
    expertise: Optional[str] = None  # Optional field for coach's expertise
    affiliations: Optional[str] = None  # Optional field for gym or team affiliations
    coach_bio: Optional[str] = None  # Optional field for a short bio about the coach
    price: Optional[int] = Field(
        default=None,
        ge=5,  # Minimum value for price
        le=99,  # Maximum value for price
        nullable=True
    )    

    class Config:
        json_schema_extra = {
            "example": {
                "expertise": "Leglocks, Escapes, Takedowns",
                "affiliations": "Brazilian Jiu-Jitsu Gym",
                "coach_bio": "Experienced BJJ coach with 10 years of teaching."
            }
        }

class Response_forPublic_CoachProfile(BaseModel):
    username: str
    expertise: Optional[List[str]]  # E.g., 'Leglocks, Escapes, Takedowns'
    affiliation: Optional[str] = None
    coach_bio: Optional[str]  # Bio specific to their coaching experience

    class Config:
        from_attributes = True

class Response_forAccountHolder_CoachProfile(Response_forPublic_CoachProfile):
    price: int
    accepting_responses: bool

class Response_forSelf_CoachProfile(Response_forAccountHolder_CoachProfile):
    settings: str = "<Some user specific settings e.g., settings>"

class StudentCreateModel(BaseModel):
    areas_working_on: Optional[str] = None  # Optional field to describe areas the student is working on

    class Config:
        json_schema_extra = {
            "example": {
                "areas_working_on": "Guard Passing, Sweeps"
            }
        }


class StudentModel(BaseModel):
    student_id: uuid.UUID
    user_id: uuid.UUID  # Foreign key to User
    areas_working_on: Optional[str]  # E.g., 'Guard Passing, Sweeps'

    class Config:
        from_attributes = True