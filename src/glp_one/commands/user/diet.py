import typer

from glp_one.models import User, DailyLog
from typing import Annotated


app = typer.Typer()


@app.command("diet")
def get_diet(username: Annotated[str, typer.Argument(help="The name of the user profile to calculate the diet for.")]):
    "Estimate the daily caloric consumption to Cut, Maintain or Bulk"
    user: User = User.load_or_create(username)
    
    if not user.data_path.exists():
        print(f"{username} doesn't exist.")
        return

    if len(user.user_log.logs) < 2:
        print(f"Not enough data.")
        return
    
    cut: int
    maintain: int
    bulk: int
    cut, maintain, bulk= user.calculate_goal()
    print(f"Cut: {cut}\nMaintain: {maintain}\nBulk: {bulk}")
