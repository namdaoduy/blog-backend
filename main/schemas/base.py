from flask import jsonify
from marshmallow import post_dump, Schema


class BaseSchema(Schema):
    def __init__(self, strict=True, **kwargs):
        super(Schema, self).__init__(strict=strict, **kwargs)

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        return {
            'data': data,
            'success': True
        }

    def jsonify(self, obj, many=True):
        return jsonify(self.dump(obj, many).data)
