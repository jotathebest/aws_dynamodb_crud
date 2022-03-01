from chalice import Response

from chalicelib.responses.users import UsersCreationErrors, UsersRetrievalErrors, UserUpdateErrors
from chalicelib.schemas.users import UserSchema
from chalicelib.cloud_db.aws_db import PorterDB
from chalicelib.utils.utils import get_int


class HandlerUser:

    def __init__(self):
        self.porter_db = PorterDB()

    def create_user(self, user_id: str, user_data: dict) -> Response:
        # The body of the request should be a valid user record
        user_validation = UserSchema.validate_schema(user_data)
        if not user_validation["is_valid"]:
            return UsersCreationErrors.user_schema_is_not_valid(user_validation["errors"])
        # A 400 will be returned when the json request is missing
        if user_data is None or len(user_data) == 0:
            return UsersCreationErrors.json_body_is_empty()
        # A 400 will be returned to the case where the userid in the json request does not match the URI
        if int(user_id) != user_data["userId"]:
            return UsersCreationErrors.user_ids_do_not_match()

        user = user_validation["user"]
        return self.porter_db.add_user(user)

    def retrieve_user(self, user_id: str) -> Response:
        user_id = get_int(user_id)
        if user_id is None:
            return UsersRetrievalErrors.user_id_is_not_valid()

        return self.porter_db.get_user(str(user_id))

    def delete_user(self, user_id: str) -> Response:
        user_id = get_int(user_id)
        if user_id is None:
            return UsersRetrievalErrors.user_id_is_not_valid()
        return self.porter_db.delete_user(str(user_id))

    def update_user(self, user_id: str, user_data: dict) -> Response:
        # The body of the request should be a valid user record
        user_validation = UserSchema.validate_schema(user_data)
        if not user_validation["is_valid"]:
            return UserUpdateErrors.user_schema_is_not_valid(user_validation["errors"])
        # A 400 will be returned when the json request is missing
        if user_data is None or len(user_data) == 0:
            return UserUpdateErrors.json_body_is_empty()
        # A 400 will be returned to the case where the userid in the json request does not match the URI
        if int(user_id) != user_data["userId"]:
            return UserUpdateErrors.user_ids_do_not_match()

        user = user_validation["user"]
        return self.porter_db.update_user(user)

