import typer

from .add import app as add_app
from .delete import app as delete_app
from .rename import app as rename_app
from .get import app as get_app
from .list import app as list_app
from .compute import app as compute_app
from .diet import app as diet_app

app = typer.Typer()

app.add_typer(add_app)
app.add_typer(delete_app)
app.add_typer(rename_app)
app.add_typer(get_app)
app.add_typer(list_app)
app.add_typer(compute_app)
app.add_typer(diet_app)