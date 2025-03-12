from pydantic import BaseModel
import uuid
from datetime import datetime

class User(BaseModel):
    uid: uuid.UUID
    name: str
    belt: str
    started_at: datetime
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    name: str
    belt: str
    started_at: str

class UserUpdateModel(BaseModel):
    name: str
    belt: str

