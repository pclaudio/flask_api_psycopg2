from flask import g, request
from http import HTTPStatus


def all_members() -> tuple[dict, int]:
    query = "SELECT * FROM membros"

    cursor = g.db_cursor
    cursor.execute(query)
    data = cursor.fetchall()

    members = [member for member in data]

    return {"data": members}, HTTPStatus.OK


def create_member() -> tuple[dict, int]:
    query = "INSERT INTO membros (nome, cpf) VALUES (%s , %s)"

    data = request.get_json()
    member = (data.get("nome"), data.get("cpf"))

    cursor = g.db_cursor
    cursor.execute(query, member)

    return {"message": "member created"}, HTTPStatus.CREATED
