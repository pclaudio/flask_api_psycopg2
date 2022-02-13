from app.controllers import all_members, create_member
from app.decorators import verify_keys
from flask import Blueprint

member_blueprint = Blueprint("member", __name__, url_prefix="/membros")


@member_blueprint.get("")
def get_all_members() -> tuple[dict, int]:
    return all_members()


@member_blueprint.post("")
@verify_keys(["nome", "cpf"])
def post_create_member() -> tuple[dict, int]:
    return create_member()
