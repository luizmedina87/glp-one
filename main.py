import typer

from glp_one.commands.user import app as user_app
from glp_one.commands.log import app as log_app


app = typer.Typer()

app.add_typer(user_app, name="user")
app.add_typer(log_app, name="log")


if __name__ == "__main__":
    app()