import click

from flask import current_app, Flask, g
from flask.cli import with_appcontext
from psycopg2 import connect
from psycopg2.extras import DictCursor
from typing import Any


def get_db_connection() -> Any:
    if "db_connection" not in g:
        g.db_connection = connect(
            host=current_app.config["DB_HOSTNAME"],
            database=current_app.config["DB_DATABASE"],
            user=current_app.config["DB_USERNAME"],
            password=current_app.config["DB_PASSWORD"],
            cursor_factory=DictCursor
        )

    return g.db_connection


def get_db_cursor() -> Any:
    if "db_cursor" not in g:
        g.db_cursor = get_db_connection().cursor()

    return g.db_cursor


def close_db(exception: Exception = None) -> None:
    db_connection = g.pop("db_connection", None)
    db_cursor = g.pop("db_cursor", None)

    if db_cursor is not None:
        db_cursor.close()

    if db_connection is not None:
        db_connection.commit()
        db_connection.close()


def init_db() -> None:
    db_cursor = get_db_cursor()

    with current_app.open_resource("schema.sql") as file:
        db_cursor.execute(file.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
