from enum import Enum
from pydantic import BaseModel

# Validators
class Belts(Enum): # '_' denotes a helper class, might be moved to a different file later.
    white = 'white'
    blue = 'blue'
    purple = 'purple'
    brown = 'brown'
    black = 'black'
    red = 'red'

# User classes
class Strengths(BaseModel): # Again, this a helper class but for adding complex fields to the user
    area: str

class BJJUser(BaseModel):
    id: int
    name: str
    belt: str
    gym: str
    strengths: list[Strengths] = []

