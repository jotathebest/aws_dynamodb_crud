from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    username = fields.Str(validate=validate.Length(min=1), required=True)
    email = fields.Str(validate=validate.Email(), required=True)
    userId = fields.Integer(required=True, strict=True)
    groupName = fields.Str(validate=validate.Length(min=1), required=True)

    @staticmethod
    def validate_schema(input_data: dict) -> dict:
        try:
            user = UserSchema().load(input_data)
            return {"is_valid": True, "user": user}
        except ValidationError as err:
            return {"is_valid": False, "errors": err.messages}
