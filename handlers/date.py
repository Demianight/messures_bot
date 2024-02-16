from datetime import datetime


def normalize_date(d: str):
    raw_date = d.split()
    return datetime(
        year=int(raw_date.pop()),
        month=int(raw_date.pop()),
        day=int(raw_date.pop()),
        hour=int(raw_date[0].split(':')[0]),
        minute=int(raw_date[0].split(':')[1])
    )
