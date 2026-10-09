import typer

from glp_one.models import User
from typing import Annotated


app = typer.Typer()

@app.command()
def delete(username: Annotated[str, typer.Argument()]):
    user = User.load_or_create("Luiz")
    if user.data_path.exists():
        user.delete()
        print(f"{username} deleted.")
    else:
        print(f"{username} doesn't exist.")