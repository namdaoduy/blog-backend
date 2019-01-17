from flask import jsonify
from marshmallow import post_dump, Schema


class BaseSchema(Schema):

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        return {
            'data': data,
            'success': True
        }

    def jsonify(self, obj, many=True):
        return jsonify(self.dump(obj, many).data)


class EmptySchema(BaseSchema):

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        return {
            'data': None
        }
