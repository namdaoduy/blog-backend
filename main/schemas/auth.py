from marshmallow import fields

from main.schemas.base import BaseSchema


class AccessTokenSchema(BaseSchema):
    user_id = fields.String(required=True)
    access_token = fields.String(required=True)

