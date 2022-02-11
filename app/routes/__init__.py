from app.routes.member_route import member_blueprint
from flask import Blueprint

root_blueprint = Blueprint("root", __name__, url_prefix="/")
root_blueprint.register_blueprint(member_blueprint)
