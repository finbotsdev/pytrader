# encoding: utf-8

from flask import Flask, g
import pytrader.model as model
import os
from werkzeug.utils import import_string

def create_app():
    app = Flask(__name__)
    app.config.from_object(import_string(os.environ.get('FLASK_CFG'))())
    app.app_context().push()
    model.init_app(app)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app

if __name__ == "app":
    app = create_app()
