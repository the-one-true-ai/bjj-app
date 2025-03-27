import uuid
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, List
from src.users.validators import Role, Belt, validate_birthdate

#TODO: Add model_config for each

# Inputs

class Input_forSelf_CoachCreateModel(BaseModel):
    # Mandatory Coach fields

    # Optional Coach fields
    expertise: Optional[List[str]] = Field(default= lambda: [""], description="An array of strings of expertise areas of the coach.")
    affiliations: Optional[List[str]] = Field(default= lambda: [""], description="An array of strings of the coaches affiliations.")
    coach_bio: Optional[str] = Field(default=None, description="The coaches bio.") 
    price: Optional[int] = Field(default=None, ge=5, le=99, description="Coach price per session (5-99).") 

class Input_forSelf_StudentCreateModel(BaseModel):
    # Mandatory Coach fields

    # Optional Student fields
    areas_working_on: Optional[List[str]] = Field(default= lambda: [""], description="An array of strings of the areas that the student is working on.")

class Input_forPublic_UserCreateSchema(Input_forSelf_CoachCreateModel, Input_forSelf_StudentCreateModel):
    # Mandatory User fields
    username: str = Field(min_length=5, max_length=30, description="The username of the user.")
    email: str = Field(min_length=10, max_length=40, description="The email address of the user.")
    password: str = Field(min_length=6, max_length=50, description="The user's password.")
    role: Role = Role.Student

    # Optional User fields
    height: Optional[int] = Field(default=None, ge=75, le=300, description="User's height in cm (75-300cm).")
    weight: Optional[int] = Field(default=None, ge=50, le=300, description="User's weight in kg (50-300kg).")
    birthdate: Optional[date] = Field(default=None, description="The users birthday (must be 18+).") #TODO Add validation to make them 18+
    belt: Belt = Field(default=Belt.White, description="The users current belt.")

    @field_validator("birthdate")
    @classmethod
    def validate_birthdate_field(cls, value: Optional[date]) -> Optional[date]:
        return validate_birthdate(value)

# Responses

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

class SudentModel(BaseModel): # ! This will change soon
    student_id: uuid.UUID
    user_id: uuid.UUID  # Foreign key to User
    areas_working_on: Optional[List[str]]  # E.g., 'Guard Passing, Sweeps'

    class Config:
        from_attributes = True


class UserUpdateModel(BaseModel): # ! Will be going soon. Split out each field for fact tables
    username: Optional[str] = None
    role: Optional[Role] = None        