from flask import Flask
import os
from werkzeug.utils import import_string

app = Flask(__name__)
app.config.from_object(import_string(os.environ.get('FLASK_CFG'))())

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"