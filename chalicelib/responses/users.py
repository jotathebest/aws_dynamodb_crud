from chalice import Response
from chalicelib.responses.base import base_error_json, base_success_json


class UsersCreationErrors:

    @staticmethod
    def json_body_is_empty() -> Response:
        message = "you are not sending the user data in your request"
        status_code = 400
        return base_error_json(message, status_code)

    @staticmethod
    def user_ids_do_not_match() -> Response:
        message = "user id from body does not match from the one used in the url"
        status_code = 400
        return base_error_json(message, status_code)

    @staticmethod
    def user_schema_is_not_valid(errors: str) -> Response:
        status_code = 400
        return base_error_json(errors, status_code)

    @staticmethod
    def user_already_exists() -> Response:
        message = "user already exists"
        status_code = 409
        return base_error_json(message, status_code)

    @staticmethod
    def user_default_error(status_code: int, errors: str) -> Response:
        return base_error_json(errors, status_code)


class UsersRetrievalErrors:

    @staticmethod
    def user_id_is_not_valid() -> Response:
        status_code = 400
        message = "user id is not valid"
        return base_error_json(message, status_code)

    @staticmethod
    def user_does_not_exist() -> Response:
        status_code = 404
        message = "user does not exist"
        return base_error_json(message, status_code)


class UserCreationSuccess:

    @staticmethod
    def user_added_to_dynamo_db():
        message = "user has been successfully added to the DB"
        status_code = 201
        return base_success_json(message, status_code)


class UsersRetrievalSuccess:

    @staticmethod
    def user_retrieved(user_data: dict):
        message = "user retrieved properly"
        status_code = 200
        additional_data = {"user_data": user_data}
        return base_success_json(message, status_code, additional_data=additional_data)


class UserUpdateErrors:

    @staticmethod
    def user_could_not_be_updated(errors: str):
        status_code = 500
        return base_error_json(errors, status_code)

    @staticmethod
    def json_body_is_empty() -> Response:
        message = "you are not sending the user data in your request"
        status_code = 409
        return base_error_json(message, status_code)

    @staticmethod
    def user_ids_do_not_match() -> Response:
        message = "user id from body does not match from the one used in the url"
        status_code = 409
        return base_error_json(message, status_code)

    @staticmethod
    def user_schema_is_not_valid(errors: str) -> Response:
        status_code = 400
        return base_error_json(errors, status_code)

    @staticmethod
    def user_does_not_exist():
        status_code = 404
        message = "user does not exist"
        return base_error_json(message, status_code)


class UserUpdateSuccess:

    @staticmethod
    def user_updated():
        status_code = 200
        message = "user information updated"
        return base_success_json(message, status_code)


class UserDeleteErrors:

    @staticmethod
    def user_does_not_exist():
        status_code = 404
        message = "user does not exist"
        return base_error_json(message, status_code)

    @staticmethod
    def user_id_is_not_valid() -> Response:
        status_code = 400
        message = "user id is not valid"
        return base_error_json(message, status_code)

    @staticmethod
    def user_default_error(status_code: int, errors: str) -> Response:
        return base_error_json(errors, status_code)


class UserDeleteSuccess:

    @staticmethod
    def user_deleted():
        message = "user deleted"
        status_code = 204
        return base_success_json(message, status_code)
