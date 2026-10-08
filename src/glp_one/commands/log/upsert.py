import typer

from typing import Annotated


app = typer.Typer()

@app.command()
def upsert(
        username: Annotated[str, typer.Argument()], 
        date: Annotated[str, typer.Option("--date", "-d")], 
        weight_t: Annotated[str, typer.Option("--weight", "-w", help="Weight measured as of date.")] = None, 
        calories_tm1: Annotated[int, typer.Option("--calories", "-c", help="Calories consumed in t-1")] = None
    ):
    print(f"Inserting (or updating) entry for {username} at {date} with {weight_t} {calories_tm1}")