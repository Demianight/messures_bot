from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Measure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    measure: str

    user_id: Optional[int] = Field(default=None, foreign_key='user.id')
    user: Optional['User'] = Relationship(back_populates='measures')


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tg_id: int

    measures: List[Measure] = Relationship(back_populates='user')
