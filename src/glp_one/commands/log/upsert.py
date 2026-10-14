import typer

from glp_one.models import User, DailyLog
from typing import Annotated


app = typer.Typer()

@app.command()
def upsert(
        username: Annotated[str, typer.Argument(help="The name of the user profile to upsert a log entry for.")], 
        date: Annotated[str, typer.Option("--date", "-d", help="The date of the log entry (YYYY-MM-DD format).")], 
        weight_t: Annotated[float, typer.Option("--weight", "-w", help="Weight measured as of date.")], 
        calories_tm1: Annotated[int, typer.Option("--calories", "-c", help="Calories consumed in t-1.")]
    ):
    """Insert or update a daily log entry with weight and calorie data for a user."""
    user = User.load_or_create(username)
    if not user.data_path.exists():
        print(f"{username} doesn't exist. Upsert canceled.")
        return
    new_log = DailyLog(date, weight_t, calories_tm1)
    user.user_log.upsert_entry(new_log)
    user.save()
    print(f"Upserted entry for {username} at {date} with {weight_t} {calories_tm1}")