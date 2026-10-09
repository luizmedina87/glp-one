import typer

from .add import app as add_app
from .delete import app as delete_app
from .rename import app as rename_app
from .get import app as get_app
from .list import app as list_app
from .chart import app as chart_app
from .compute import app as compute_app

app = typer.Typer()

app.add_typer(add_app)
app.add_typer(delete_app)
app.add_typer(rename_app)
app.add_typer(get_app)
app.add_typer(list_app)
app.add_typer(chart_app)
app.add_typer(compute_app)