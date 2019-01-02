from functools import wraps
import jwt
from flask import request, abort
from main.cfg.local import config


def authorization(fn):
    """ Check Authorization Header, add user_id as 1st param """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        user_id = None
        data = request.headers['Authorization'].encode('ascii', 'ignore')
        token = str.replace(str(data), 'Bearer ', '')
        try:
            user_id = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])['user_id']
        except:
            abort(401)
        return fn(user_id, *args, **kwargs)
    return wrapper
