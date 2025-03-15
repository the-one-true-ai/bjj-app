from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


class Gym(SQLModel, table=True):
    __tablename__ = "DimGym"

    # Need to add Optional to these
    gym_id: uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, nullable=False, default=uuid.uuid4))
    gym_name: str
    address: str
    website: str
    affiliation: str

    def __repr__(self):
        return f"Gym {self.gym_name}"