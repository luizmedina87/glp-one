import typer

from glp_one.models import User
from typing import Annotated


app = typer.Typer()

@app.command()
def add(username: Annotated[str, typer.Argument()]):
    user = User.load_or_create(username)
    if user.data_path.exists():
        print(f"{username} already exists at {user.data_path}")
    else:
        user.save()
        print(f"{username} saved at {user.data_path}")
    