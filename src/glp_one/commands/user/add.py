import typer

from typing import Annotated


app = typer.Typer()

@app.command()
def add(username: Annotated[str, typer.Argument()]):
    print(f"Adding {username}")