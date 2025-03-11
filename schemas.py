from enum import Enum
from pydantic import BaseModel

class BeltLevels(Enum):
    WHITE = 'white'
    BLUE = 'blue'
    PURPLE = 'purple'
    BROWN = 'brown'
    BLACK = 'black'
    RED = 'red'

class User(BaseModel):
    id: int
    name: str
    belt: str
    gym: str
