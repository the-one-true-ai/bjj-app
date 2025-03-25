from enum import Enum

class Role(str, Enum):
    Student = "Student"
    Coach = "Coach"
    Both = "Both"

class Belt(str, Enum):
    White = "White"
    Blue = "Blue"
    Purple = "Purple"
    Brown = "Brown"
    Black = "Black"
    Coral = "Coral"