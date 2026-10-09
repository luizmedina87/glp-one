import typer

from typing import Annotated
from glp_one.models import User


app = typer.Typer()

@app.command()
def delete(
    username: Annotated[str, typer.Argument()], 
    date: Annotated[str, typer.Option("--date", "-d")], 
    ):
    user = User.load_or_create(username)
    if not user.data_path.exists():
        print(f"{username} doesn't exist. Delete canceled.")
        return
    deleted = user.user_log.delete_entry(date)
    if deleted:
        print(f"Deleted entry for {username} at {date}")
        user.save()
    else:
        print(f"Date {date} doesn't exist in user log.")
    