import matplotlib.pyplot as plt

from database.models import Measure


def create_graph(measures: list[Measure]):
    dates = [measure.date for measure in measures]
    vals = [int(measure.measure.split()[0]) for measure in measures]

    print(vals)

    plt.figure(figsize=(10, 6))
    plt.plot(dates, vals, marker='o', linestyle='-')

    plt.xlabel('Date')
    plt.ylabel('Measure')
    plt.title('Measure vs Date')

    plt.xticks(rotation=45)

    plt.grid(True)
    plt.tight_layout()

    path = 'measure_plot.jpg'
    plt.savefig(path, dpi=300)

    return path
