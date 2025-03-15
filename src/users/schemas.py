from pydantic import BaseModel, Field
import uuid
from datetime import datetime

# Base schema for common fields (used for both creation and update)
class UserBaseSchema(BaseModel):
    email: str
    password: str = Field(min_length=5, max_length=30)

class FullUserSchema(UserBaseSchema):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

# User schema for updating (only fields that can be updated)
class UserUpdateSchema(UserBaseSchema):
    email: str

# User schemas to be returned
class UserResponseSchema(BaseModel):
    uid: uuid.UUID
    email: str
    created_at: datetime
    updated_at: datetime

