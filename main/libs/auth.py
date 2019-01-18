from functools import wraps
import jwt
from flask import request
from main import config
from main import errors


def authorization(fn):
    """Check Authorization Header, add user_id as 1st param"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            raise errors.Unauthorized()
        data = request.headers['Authorization'].encode('ascii', 'ignore')
        token = str.replace(str(data), 'Bearer ', '')
        try:
            user_id = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])['user_id']
        except Exception:
            raise errors.Unauthorized()
        return fn(user_id, *args, **kwargs)
    return wrapper
