from flask import Blueprint
from http import HTTPStatus

member_blueprint = Blueprint("member", __name__, url_prefix="/membros")


@member_blueprint.get("")
def hello():
    return "Hello, Flask!", HTTPStatus.OK
