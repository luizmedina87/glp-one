import typer

from typing import Annotated


app = typer.Typer()

@app.command()
def get(username: Annotated[str, typer.Argument()]):
    print(f"Getting data for {username}")