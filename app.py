from chalice import Chalice, Response

from chalicelib.handlers.handler_group import HandlerGroup
from chalicelib.handlers.handler_user import HandlerUser

app = Chalice(app_name="porter")


@app.route("/")
def index():
    return {"hello": "world"}


@app.route("/users/{user_id}", methods=["POST"])
def add_user(user_id: str) -> Response:
    user_data = app.current_request.json_body
    handler = HandlerUser()
    return handler.create_user(user_id, user_data)


@app.route("/users/{user_id}", methods=["GET"])
def get_user(user_id: str):
    handler = HandlerUser()
    return handler.retrieve_user(user_id)


@app.route("/users/{user_id}", methods=["PUT"])
def get_user(user_id: str):
    user_data = app.current_request.json_body
    handler = HandlerUser()
    return handler.update_user(user_id, user_data)


@app.route("/users/{user_id}", methods=["DELETE"])
def delete_user(user_id: str):
    handler = HandlerUser()
    return handler.delete_user(user_id)


@app.route("/groups/{group_name}", methods=["GET"])
def get_users_from_group(group_name: str):
    handler = HandlerGroup()
    return handler.get_users_from_group(group_name)


@app.route("/groups/{group_name}", methods=["PUT"])
def update_users_from_group(group_name: str):
    user_data = app.current_request.json_body
    handler = HandlerGroup()
    return handler.update_users_group(group_name, user_data)


@app.route("/groups/{group_name}", methods=["DELETE"])
def delete_users_from_group(group_name: str):
    handler = HandlerGroup()
    return handler.delete_users_from_group(group_name)
