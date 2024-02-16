from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from database.config import engine

from database.models import Measure, User


def create_measure(measure: Measure) -> None:
    with Session(engine) as db:
        db.add(measure)
        db.commit()


def get_user(tg_id: int) -> Optional[User]:
    with Session(engine) as db:
        return db.get(User, tg_id)


def create_user(user: User) -> None:
    if get_user(user.tg_id):
        return

    with Session(engine) as db:
        db.add(user)
        db.commit()


def _get_measures(tg_id: int) -> list[Measure]:
    with Session(engine) as session:
        statement = select(Measure).where(Measure.user_id == tg_id)
        measures = session.exec(statement)

        return [measure for measure in measures]


def get_measures(tg_id: int) -> list[tuple[list[int], datetime]]:
    def normalize_measure(raw: Measure) -> tuple[list[int], datetime]:
        return list(
            map(int, raw.measure.split())
        ), raw.date

    measures = _get_measures(tg_id)
    return [
        normalize_measure(measure) for measure in measures
    ]
