from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class BlogSchema(BaseSchema):
    title = fields.String(validate=[validate.Length(min=10, max=100)])
    body = fields.String(validate=[validate.Length(min=1000)])

