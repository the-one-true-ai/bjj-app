import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import String

# FactUser (Base Table)
class FactUser(SQLModel, table=True):
    __tablename__ = "fact_user"

    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))

    name: str
    email: str = Field(default="unknown@example.com", sa_column=Column(String, nullable=False))  # Default placeholder email
    password: str
    first_name: str = Field(default="Unknown", sa_column=Column(String, nullable=False))  # Default placeholder first name
    last_name: str = Field(default="User", sa_column=Column(String, nullable=False))  # Default placeholder last name
    is_verified: bool = False
    belt: str
    started_at: Optional[datetime] = None
    preferred_ruleset: Optional[str] = Field(default="Both", sa_column=Column(String, nullable=False))  # Gi, No-Gi, or Both
    bio: Optional[str] = None
    social_links: Optional[str] = None
    competition_history: Optional[str] = None
    associations: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))  
    role: str = Field(default="Student", sa_column=Column(String, nullable=False))  # Use String from sqlalchemy
    height: Optional[float] = None
    weight: Optional[float] = None
    birthdate: Optional[int] = None
    profile_picture: Optional[str] = Field(default="some_default_picture.jpeg", sa_column=Column(String, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  
    status: Optional[str] = Field(default="Active", sa_column=Column(String, nullable=False))    
    date_deactivated: Optional[datetime] = None    


    # Relationships
    coach_info: Optional["FactCoach"] = Relationship(back_populates="user")
    student_info: Optional["FactStudent"] = Relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.name}>"


# FactCoach (Coaches Only)
class FactCoach(SQLModel, table=True):
    __tablename__ = "fact_coach"

    coach_id: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    uid: uuid.UUID = Field(foreign_key="fact_user.uid", ondelete="CASCADE")

    expertise: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))    # Leglocks, Pins, Escapes, etc.
    affiliations: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))    # List of gyms
    coach_bio: Optional[str] = None
    languages: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))  
    reviews_given: int = 0
    active_flag: bool = True # If coaches want to turn off from getting more requests

    user: FactUser = Relationship(back_populates="coach_info")


# FactStudent (Students Only)
class FactStudent(SQLModel, table=True):
    __tablename__ = "fact_student"

    student_id: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    uid: uuid.UUID = Field(foreign_key="fact_user.uid", ondelete="CASCADE")

    areas_working_on: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))    # Techniques being focused on
    preferred_coach_style: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))  

    user: FactUser = Relationship(back_populates="student_info")