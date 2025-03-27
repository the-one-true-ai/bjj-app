from enum import Enum
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Optional

def validate_birthdate(value: Optional[date]) -> Optional[date]:
    if value is None:
        return value

    # Ensure the user is at least 18 years old
    min_age_date = date.today() - relativedelta(years=18)
    if value > min_age_date:
        raise ValueError("User must be at least 18 years old.")
    
    # Ensure the user is not older than 150 years
    max_age_date = date.today() - relativedelta(years=150)
    if value < max_age_date:
        raise ValueError("User must be less than 150 years old.")

    return value

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