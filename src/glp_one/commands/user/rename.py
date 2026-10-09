import typer

from glp_one.models import User
from typing import Annotated

app = typer.Typer()

@app.command()
def rename(
    old_username: Annotated[str, typer.Argument()], 
    new_username: Annotated[str, typer.Argument()]
    ):
    user = User.load_or_create(old_username)
    if user.data_path.exists():
        user.rename(new_username)
        print(f"{old_username} was renamed to {new_username}")
    else:
        print(f"{old_username} does not exist.")