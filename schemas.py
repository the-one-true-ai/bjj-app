from enum import Enum
from pydantic import BaseModel, validator
from typing import List  # Add this import for List typing

# Validators
class Belts(Enum): # '_' denotes a helper class, might be moved to a different file later.
    WHITE = 'white'
    BLUE = 'blue'
    PURPLE = 'purple'
    BROWN = 'brown'
    BLACK = 'black'
    RED = 'red'

class BeltsChoices(Enum): # '_' denotes a helper class, might be moved to a different file later.
    WHITE = 'White'
    BLUE = 'Blue'
    PURPLE = 'Purple'
    BROWN = 'Brown'
    BLACK = 'Black'
    RED = 'Red'

# User classes
class Strengths(BaseModel): # Again, this a helper class but for adding complex fields to the user
    area: str

class UserBase(BaseModel):
    name: str
    belt: BeltsChoices
    gym: str
    strengths: List[Strengths] = []  # Change list[Strengths] to List[Strengths]

class UserCreate(UserBase):
    @validator("belt", pre=True)
    def title_case(cls, value):
        return value.title()
    

class UserWithID(UserBase):
    id: int
