from marshmallow import fields, validate

from main.schemas.base import BaseSchema
from main import config


class BlogSchema(BaseSchema):
    id = fields.Integer()
    title = fields.String(validate=validate.Length(min=config.BLOG_TITLE_LENGTH_MIN,
                                                   max=config.BLOG_TITLE_LENGTH_MAX))
    body = fields.String(validate=validate.Length(min=config.BLOG_BODY_LENGTH_MIN,
                                                  max=config.BLOG_BODY_LENGTH_MAX))
    like = fields.Integer()
    created_at = fields.DateTime()
    user_id = fields.String()
    author = fields.String()
    picture = fields.String()
    is_liked = fields.Integer()
