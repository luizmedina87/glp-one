import typer

from typing import Annotated
from glp_one.models import User
from rich.console import Console
from rich.table import Table

app = typer.Typer()

def print_log_table(user: User) -> None:
    table = Table()
    table.add_column("Date")
    table.add_column("Weight (t)")
    table.add_column("Weight Smooth. (t)")
    table.add_column("Calories (t-1)")
    table.add_column("TDEE Est. (t-1)")
    table.add_column("TDEE Est. Smooth. (t-1)")

    for log in user.user_log.logs:
        table.add_row(
            log.entry_date.isoformat(),
            f"{log.weight_t}",
            f"{log.weight_smoothed_t}",
            f"{log.calories_tm1}",
            f"{log.tdee_t}",
            f"{log.tdee_smoothed_t}"
        )

    console = Console()
    console.print(table)

@app.command()
def get(username: Annotated[str, typer.Argument()]):
    user: User = User.load_or_create(username)
    if user.exists():
        print_log_table(user)
