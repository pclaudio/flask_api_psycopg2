from flask import request
from functools import wraps
from http import HTTPStatus


def verify_keys(trusted_keys: list[str]):
    def decorator(function):
        @wraps(function)
        def wrapper():
            data = request.get_json()

            if data is None or len(data) != len(trusted_keys):
                return {"message": "missing key(s) in the request body"}, HTTPStatus.BAD_REQUEST

            for trusted_key in trusted_keys:
                try:
                    data[trusted_key]
                except (KeyError, TypeError):
                    return {"message": "missing key(s) in the request body"}, HTTPStatus.BAD_REQUEST

            return function()

        return wrapper

    return decorator
