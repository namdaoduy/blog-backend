from flask import jsonify
from marshmallow import post_dump, Schema, fields, post_load


class BaseSchema(Schema):

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        return {
            'data': data,
            'success': True
        }

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many).data)


class ErrorSchema(Schema):

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        return {
            'error_description': data,
            'error': True
        }

    def jsonify(self, obj, many=False):
        return jsonify(self.dump(obj, many).error_description)


class EmptySchema(BaseSchema):

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        return {
            'data': None
        }


class FieldsQuerySchema(BaseSchema):
    fields = fields.String(required=False)

    @post_load
    def parse_fields(self, data):
        _fields = data.get('fields', None)
        if _fields:
            _fields = set(_fields.split(','))
            data['fields'] = _fields
        else:
            data['fields'] = set()

        return data
