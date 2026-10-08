import typer

from typing import Annotated

app = typer.Typer()

@app.command()
def rename(old_username: Annotated[str, typer.Argument()], new_username: Annotated[str, typer.Argument()]):
    print(f"{old_username} was renamed to {new_username}")