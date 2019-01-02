from marshmallow import fields

from main.schemas.base import BaseSchema


class AccessTokenSchema(BaseSchema):
    user_id = fields.String()
    access_token = fields.String()
