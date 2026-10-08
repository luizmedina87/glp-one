import typer

from typing import Annotated


app = typer.Typer()

@app.command()
def recalculate(username: Annotated[str, typer.Argument()]):
    print(f"Recalculating {username}")