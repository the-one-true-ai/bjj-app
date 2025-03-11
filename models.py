from enum import Enum
from pydantic import BaseModel, validator
from typing import List  # Add this import for List typing
from validators import check_value_range
from sqlmodel import SQLModel, Field

# Validators
class Belts(Enum): # '_' denotes a helper class, might be moved to a different file later.
    WHITE = 'White'
    BLUE = 'Blue'
    PURPLE = 'Purple'
    BROWN = 'Brown'
    BLACK = 'Black'
    RED = 'Red'

# User classes
class GymBase(SQLModel): # Again, this a helper class but for adding complex fields to the user
    head_coach: str


class Gym(GymBase, table=True):
    id: int = Field(default=None, primary_key=True)

class UserBase(BaseModel):
    name: str
    belt: Belts
    stripes: int = 0
    gym: Gym

class UserCreate(UserBase):
    @validator("belt", pre=True)
    def title_case(cls, value):
        return value.title()
    
class UserWithID(UserBase):
    id: int
