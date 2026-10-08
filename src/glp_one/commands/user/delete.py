import typer

from typing import Annotated


app = typer.Typer()

@app.command()
def delete(username: Annotated[str, typer.Argument()]):
    print(f"Deleting {username}")