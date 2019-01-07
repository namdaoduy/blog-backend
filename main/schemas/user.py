from marshmallow import fields

from main.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.String()
    name = fields.String()
    email = fields.String()
    picture = fields.String()
