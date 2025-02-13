import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'postgresql://mfoust:EulbogUuAHvQgUs9yG6DDY8BVV6MbeJi@dpg-chqvo0ik728ivvo2uhc0-a.frankfurt-postgres.render.com/acrpresources'

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove() 


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config["SQLALCHEMY_DATABASE_URI"]= "postgresql://mfoust:EulbogUuAHvQgUs9yG6DDY8BVV6MbeJi@dpg-chqvo0ik728ivvo2uhc0-a.frankfurt-postgres.render.com/acrpresources"
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app