import typer

from .delete import app as delete_app
from .upsert import app as upsert_app


app = typer.Typer()

app.add_typer(delete_app)
app.add_typer(upsert_app)