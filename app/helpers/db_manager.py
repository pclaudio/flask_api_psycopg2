import click

from flask import current_app, Flask, g
from flask.cli import with_appcontext
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


def open_db_connection() -> None:
    if "db_connection" not in g:
        g.db_connection = connect(
            host=current_app.config["DB_HOSTNAME"],
            database=current_app.config["DB_DATABASE"],
            user=current_app.config["DB_USERNAME"],
            password=current_app.config["DB_PASSWORD"],
            cursor_factory=RealDictCursor
        )

    if "db_cursor" not in g:
        g.db_cursor = g.db_connection.cursor()


def close_db_connection(exception: Exception = None) -> None:
    db_connection = g.pop("db_connection", None)
    db_cursor = g.pop("db_cursor", None)

    if db_cursor is not None:
        db_cursor.close()

    if db_connection is not None:
        db_connection.commit()
        db_connection.close()

    if exception is not None:
        current_app.logger.error(exception)


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Clear the existing data and create new tables."""
    open_db_connection()

    with current_app.open_resource("schema.sql") as file:
        g.db_cursor.execute(file.read().decode("utf8"))

    close_db_connection()

    click.echo("Initialized the database.")


def init_app(app: Flask) -> None:
    app.before_request(open_db_connection)
    app.teardown_appcontext(close_db_connection)
    app.cli.add_command(init_db_command)
