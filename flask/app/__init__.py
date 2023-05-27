from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    Config(app)
    db.init_app(app)
    CORS(app, resources=r'/*')
    app.debug = True

    return app
