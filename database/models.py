from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Messure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    messure: tuple[int, int]
