from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def _register_subpackages():
    import main.controllers


_register_subpackages()
