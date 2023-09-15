from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'burgerflipp'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')

    from .models import User, Note

    create_database(app)

    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created DB!")
