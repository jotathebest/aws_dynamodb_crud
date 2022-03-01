from chalice import Response

from chalicelib.responses.base import base_error_json, base_success_json


class GroupErrors:

    @staticmethod
    def group_does_not_exist() -> Response:
        message = "the group does not exist"
        status_code = 404
        return base_error_json(message, status_code)

    @staticmethod
    def group_does_have_members() -> Response:
        message = "the group does not have members"
        status_code = 404
        return base_error_json(message, status_code)

    @staticmethod
    def cannot_update_group_of_empty_users() -> Response:
        message = "users list cannot be empty"
        status_code = 400
        return base_error_json(message, status_code)

    @staticmethod
    def group_default_error(status_code: int, errors: str) -> Response:
        return base_error_json(errors, status_code)


class GroupSuccessQuery:

    @staticmethod
    def group_members(users: list) -> Response:
        message = "group have members"
        status_code = 200
        additional_data = {"users": users}
        return base_success_json(message, status_code, additional_data=additional_data)

    @staticmethod
    def user_groups_updated() -> Response:
        message = "users' group have been updated"
        status_code = 200
        return base_success_json(message, status_code)

    @staticmethod
    def user_from_group_deleted() -> Response:
        message = "users have been deleted"
        status_code = 200
        return base_success_json(message, status_code)
