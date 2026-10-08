import typer

from typing import Annotated


app = typer.Typer()

@app.command()
def chart(username: Annotated[str, typer.Argument()]):
    print(f"Charting complex {username} data")