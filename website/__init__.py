"""TODO"""
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# is tutorialo migrate
from flask_migrate import Migrate


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    """TODO"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key for an app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Book, Note

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)
    # is tutorialo migrate
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    """TODO"""
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
