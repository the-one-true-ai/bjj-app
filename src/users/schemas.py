from pydantic import BaseModel
import uuid
from datetime import datetime, date
from typing import Optional, List, Dict

# Base schema for common fields (used for both creation and update)
class UserBaseSchema(BaseModel):
    name: str
    email: str
    password: str
    first_name: str
    last_name: str 
    is_verified: bool = "False"
    belt: str
    started_at: Optional[datetime] = None
    preferred_ruleset: Optional[str] = "Both"  # Gi, No-Gi, or Both
    bio: Optional[str] = None
    social_links: Optional[str] = None  # Enforce valid URLs
    competition_history: Optional[str] = None
    associations: Optional[List[str]] = None
    role: str = "Student"  # Defaults to student, can be "coach", "student", or "both"
    height: Optional[float] = None
    weight: Optional[float] = None
    birthdate: Optional[date] = None
    profile_picture: Optional[str] = "some_default_picture.jpeg"

class FullUserSchema(UserBaseSchema):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: str = "Active"
    date_deactivated: Optional[datetime] = None    

# User schema for updating (only fields that can be updated)
class UserUpdateSchema(UserBaseSchema):
    # Fields that can be updated after sign-up (belt, bio, etc.)
    name: Optional[str] = None
    belt: Optional[str] = None
    preferred_ruleset: Optional[str] = None
    bio: Optional[str] = None
    social_links: Optional[str] = None
    competition_history: Optional[str] = None
    associations: Optional[List[str]] = None
    profile_picture: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    birthdate: Optional[int] = None
    role: Optional[str] = None  # Allow updating of role if necessary



# FactCoach schema (for coaches only)
class CoachSchema(BaseModel):
    coach_id: uuid.UUID
    uid: uuid.UUID
    expertise: Optional[List[str]] = None  # Leglocks, Pins, Escapes, etc.
    affiliations: Optional[List[str]] = None  # List of gyms
    coach_bio: Optional[str] = None
    languages: Optional[List[str]] = None
    reviews_given: int = 0
    active_flag: bool = True  # If coaches want to turn off from getting more requests


# FactStudent schema (for students only)
class StudentSchema(BaseModel):
    student_id: uuid.UUID
    uid: uuid.UUID
    areas_working_on: Optional[List[str]] = None  # Techniques being focused on
    preferred_coach_style: Optional[List[str]] = None


# User schema with full details (including relationships to coach and student info)
class UserDetailSchema(UserBaseSchema):
    coach_info: Optional[CoachSchema] = None
    student_info: Optional[StudentSchema] = None

