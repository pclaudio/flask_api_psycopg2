from app.helpers import init_app
from app.routes import root_blueprint
from flask import Flask
from os import getenv


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, static_folder=None)
    app.config.from_mapping(
        JSON_SORT_KEYS=False,
        DB_HOSTNAME=getenv("DB_HOSTNAME"),
        DB_DATABASE=getenv("DB_DATABASE"),
        DB_USERNAME=getenv("DB_USERNAME"),
        DB_PASSWORD=getenv("DB_PASSWORD")
    )

    if test_config:
        app.config.from_mapping(test_config)

    init_app(app)

    app.register_blueprint(root_blueprint)

    return app
