import typer

from typing import Annotated
from glp_one.models import User

app = typer.Typer()

@app.command()
def compute(username: Annotated[str, typer.Argument(help="The name of the user to run computations for.")]):
    """Recalculate smoothed weights and TDEE for an existing user."""
    user = User.load_or_create("Luiz")
    if user.data_path.exists():
        user.load()
        user.update()
        print(f"Recalculated {username}")
        return
    print(f"Nothing to compute.")