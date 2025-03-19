from enum import Enum

class Role(str, Enum):
    Student = "Student"
    Coach = "Coach"
    Both = "Both"
