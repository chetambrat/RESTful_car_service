from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app(debug=True):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123qwesecrethash'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    return app
