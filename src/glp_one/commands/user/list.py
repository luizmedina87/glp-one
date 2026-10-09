import typer

from glp_one.config import get_data_dir


app = typer.Typer()

@app.command("list")
def list_users():
    user_list = [f.name[:-5] for f in get_data_dir().iterdir() if f.is_file()]
    for user in user_list:
        print(user)