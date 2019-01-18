from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class BlogSchema(BaseSchema):
    id = fields.Integer()
    title = fields.String(validate=validate.Length(min=10, max=100))
    body = fields.String(validate=validate.Length(min=1000))
    like = fields.Integer()
    created_at = fields.DateTime()
    user_id = fields.String()
    author = fields.String()
    picture = fields.String()
