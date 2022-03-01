import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from chalice import Response

from chalicelib.responses.groups import GroupErrors, GroupSuccessQuery
from chalicelib.responses.users import UsersCreationErrors, UserCreationSuccess, UsersRetrievalSuccess, \
    UserUpdateSuccess, UserUpdateErrors, UserDeleteErrors, UserDeleteSuccess, UsersRetrievalErrors


class PorterDB:
    def __init__(self):
        aws_access_key_id = os.environ.get("CLIENT_ACCESS_KEY")
        aws_secret_access_key = os.environ.get("CLIENT_SECRET_ACCESS_KEY")
        dynamodb = boto3.resource("dynamodb",
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
        self.table = dynamodb.Table("porterUsers")

    def _get_user_data_from_aws(self, user_id):
        user_data = self.get_user(user_id)
        return user_data.body.get("user_data")

    def add_user(self, user: dict) -> Response:
        try:
            user_id = str(user["userId"])
            user_data = self._get_user_data_from_aws(user_id)
            if user_data:
                return UsersCreationErrors.user_already_exists()

            self.table.put_item(Item={
                'userId': user_id,
                "username": user["username"],
                "email": user["email"],
                "groupName": user["groupName"]
            })
            return UserCreationSuccess.user_added_to_dynamo_db()
        except Exception as exc:
            return UsersCreationErrors.user_default_error(500, str(exc))

    def get_user(self, user_id: str) -> Response:
        response = self.table.query(
            KeyConditionExpression=Key("userId").eq(str(user_id))
        )
        user_data = response.get('Items', None)
        print(user_data)
        if user_data is None or len(user_data) == 0:
            return UsersRetrievalErrors.user_does_not_exist()
        return UsersRetrievalSuccess.user_retrieved(user_data)

    def update_user(self, user: dict) -> Response:
        try:
            user_id = str(user["userId"])
            user_data = self._get_user_data_from_aws(user_id)
            if user_data is None:
                return UserUpdateErrors.user_does_not_exist()

            self.table.update_item(
                Key={
                    "userId": user_id,
                },
                UpdateExpression="set username=:n, groupName=:g, email=:e",
                ExpressionAttributeValues={
                    ":n": user["username"],
                    ":g": user["groupName"],
                    ":e": user["email"]
                }
            )
            return UserUpdateSuccess.user_updated()
        except Exception as exc:
            return UserUpdateErrors.user_could_not_be_updated(str(exc))

    def delete_user(self, user_id: str) -> Response:
        try:
            user_data = self._get_user_data_from_aws(user_id)
            if user_data is None or len(user_data) == 0:
                return UserDeleteErrors.user_does_not_exist()
            self.table.delete_item(
                Key={
                    'userId': user_id,
                }
            )
            return UserDeleteSuccess.user_deleted()
        except Exception as exc:
            return UserDeleteErrors.user_default_error(500, str(exc))

    def get_users_with_common_groups(self, group_name: str) -> Response:
        try:
            response = self.table.scan(
                FilterExpression=Attr('groupName').eq(group_name)
            )
            items = response.get("Items")
            if items is None:
                return GroupErrors.group_does_not_exist()
            if len(items) == 0:
                return GroupErrors.group_does_have_members()
            user_names = [user["username"] for user in items]
            return GroupSuccessQuery.group_members(user_names)
        except Exception as exc:
            return GroupErrors.group_default_error(500, str(exc))

    def update_users_group(self, group_name: str, user_names: list):
        try:
            response = self.table.scan(
                FilterExpression=Attr('username').is_in(user_names)
            )
            items = response.get("Items")
            if items is None:
                return GroupErrors.group_does_not_exist()

            users_to_update = list(filter(lambda x: x["username"] in user_names, items))
            with self.table.batch_writer() as batch:
                for user in users_to_update:
                    user_id = user["userId"]
                    batch.put_item(
                        Item={
                            'userId': user_id,
                            "username": user["username"],
                            "email": user["email"],
                            "groupName": group_name
                        }
                    )
            return GroupSuccessQuery.user_groups_updated()
        except Exception as exc:
            return GroupErrors.group_default_error(500, str(exc))

    def delete_users_from_group(self, group_name: str):
        try:
            response = self.table.scan(
                FilterExpression=Attr('groupName').eq(group_name)
            )
            items = response.get("Items")
            if items is None or len(items) == 0:
                return GroupErrors.group_does_have_members()

            with self.table.batch_writer() as batch:
                for user in items:
                    if user["groupName"] == group_name:
                        user_id = user["userId"]
                        batch.delete_item(
                            Key={
                                "userId": user_id
                            }
                        )
            return GroupSuccessQuery.user_from_group_deleted()
        except Exception as exc:
            return GroupErrors.group_default_error(500, str(exc))
