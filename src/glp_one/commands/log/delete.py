import typer

from typing import Annotated


app = typer.Typer()

@app.command()
def delete(
    username: Annotated[str, typer.Argument()], 
    date: Annotated[str, typer.Option("--date", "-d")], 
    ):
    print(f"Deleting entry for {username} at {date}")