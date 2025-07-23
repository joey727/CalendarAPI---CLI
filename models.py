import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class Event(SQLModel, table=True):
    """Model representing an event in the system. """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)
