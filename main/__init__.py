from flask import Flask
from flask_cors import CORS

from main.config import config

app = Flask(__name__)
app.config.from_object(config)
CORS(app)


def _register_subpackages():
    import main.errors
    import main.controllers


_register_subpackages()
