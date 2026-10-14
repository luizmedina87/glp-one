import typer

from typing import Annotated
from glp_one.models import User

app = typer.Typer()

@app.command()
def compute(username: Annotated[str, typer.Argument()]):
    user = User.load_or_create("Luiz")
    if user.data_path.exists():
        user.load()
        user.update()
        print(f"Recalculated {username}")
        return
    print(f"Nothing to compute.")