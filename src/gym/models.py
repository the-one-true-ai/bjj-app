from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


class Gym(SQLModel, table=True):
    __tablename__ = "DimGym"

    gym_id = uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    gym_name: str
    address: str
    website: str
    affiliation: str

    def __repr__(self):
        return f"Gym {self.gym_name}"