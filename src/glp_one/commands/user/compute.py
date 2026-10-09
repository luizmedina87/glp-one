import typer

from typing import Annotated


app = typer.Typer()

@app.command()
def compute(username: Annotated[str, typer.Argument()]):
    print(f"Recalculating {username}")