from enum import Enum
from pydantic import BaseModel

class BeltLevels(Enum):
    white = 'white'
    blue = 'blue'
    purple = 'purple'
    brown = 'brown'
    black = 'black'
    red = 'red'


class Strengths(BaseModel):
    area: str

class BJJUser(BaseModel):
    id: int
    name: str
    belt: str
    gym: str
    strengths: list[Strengths] = []