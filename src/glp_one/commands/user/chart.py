import typer
import plotext as plt

from typing import Annotated
from glp_one.models import User
from datetime import datetime, time


app = typer.Typer()


def plot_weight(username: str) -> None:
    user = User.load_or_create(username)

    plotted_logs = [
        (int(log.entry_date.strftime("%Y%m%d")), float(log.weight_t))
        for log in user.user_log.logs
        if log.weight_t is not None
    ]

    timestamps, weights = zip(*plotted_logs)
    print(timestamps)
    print(weights)
    fig = plt.figure
    fig.clear()
    fig.theme("matrix")
    fig.title(f"Weight History — {username}")
    fig.label("Date", axis="x")
    fig.label("Weight", axis="y")
    sig = fig.signal(list(timestamps), list(weights), marker="fhd").lines()
    fig.draw(sig)
    fig.show()


def plot_calories(username: str) -> None:
    ...


@app.command()
def chart(
    username: Annotated[str, typer.Argument()],
    weight: Annotated[bool, typer.Option("--wheight", "-w")] = False,
    calories: Annotated[bool, typer.Option("--calories", "-c")] = False
    ):
    if weight:
        plot_weight(username)
    if calories:
        plot_calories(username)
