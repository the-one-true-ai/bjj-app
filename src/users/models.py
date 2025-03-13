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
    belt: str
    started_at: datetime
    preferred_ruleset: Optional[str] = Field(default="Both", sa_column=Column(String, nullable=False))  # Gi, No-Gi, or Both
    bio: Optional[str] = None
    social_links: Optional[str] = None
    competition_history: Optional[str] = None
    associations: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))  
    role: str = Field(default="student", sa_column=Column(String, nullable=False))  # Use String from sqlalchemy
    verified: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    profile_picture: Optional[str] = Field(default="some_default_picture.jpeg", sa_column=Column(String, nullable=False))


    # Relationships
    coach_info: Optional["FactCoach"] = Relationship(back_populates="user")
    student_info: Optional["FactStudent"] = Relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.name}>"


# FactCoach (Coaches Only)
class FactCoach(SQLModel, table=True):
    __tablename__ = "fact_coach"

    coach_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    uid: uuid.UUID = Field(foreign_key="fact_user.uid", ondelete="CASCADE", sa_column=Column(nullable=False))

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

    student_id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    uid: uuid.UUID = Field(foreign_key="fact_user.uid", ondelete="CASCADE")

    areas_working_on: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))    # Techniques being focused on
    preferred_coach_style: Optional[List[str]] = Field(sa_column=Column(pg.ARRAY(String), nullable=True))  

    user: FactUser = Relationship(back_populates="student_info")