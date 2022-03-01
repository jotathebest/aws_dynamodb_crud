from chalice import Response

from chalicelib.cloud_db.aws_db import PorterDB
from chalicelib.responses.groups import GroupErrors


class HandlerGroup:
    def __init__(self):
        self.porter_db = PorterDB()

    def get_users_from_group(self, group_name: str) -> Response:
        if not group_name:
            GroupErrors.group_default_error(400, "group name cannot be empty")
        return self.porter_db.get_users_with_common_groups(group_name)

    def update_users_group(self, group_name: str, user_data: dict) -> Response:
        users = user_data.get("users")
        if users is None or len(users) == 0:
            return GroupErrors.cannot_update_group_of_empty_users()
        return self.porter_db.update_users_group(group_name, users)

    def delete_users_from_group(self, group_name: str) -> Response:
        return self.porter_db.delete_users_from_group(group_name)
