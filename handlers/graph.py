from datetime import datetime

import matplotlib.pyplot as plt
from aiogram.types import FSInputFile

from database.models import Measure
from main import GRAPHS_FOLDER


def create_graph(measures: list[Measure], tg_id: int):
    measures.sort(key=lambda measure: measure.date)

    dates = [measure.date for measure in measures]
    vals = [list(map(int, measure.measure.split())) for measure in measures]

    print(vals)

    plt.figure(figsize=(10, 6))
    plt.plot(dates, vals, marker='o', linestyle='-')

    plt.xlabel('Date')
    plt.ylabel('Measure')
    plt.title('Measure vs Date')

    plt.xticks(rotation=45)

    plt.grid(True)
    plt.tight_layout()

    now = datetime.now()

    name = f'graph_{now}_{tg_id}.jpg'
    plt.savefig(GRAPHS_FOLDER / name, dpi=300)

    return name


def upload_graph(name: str):
    return FSInputFile(GRAPHS_FOLDER / name, filename=name)
