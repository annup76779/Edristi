from flask import Flask, current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
crypt = Bcrypt()

def create_app(config_cls = None):
    app  = Flask(__name__) # creating the app

    # import the custom configurations for the app
    import configmodule
    if config_cls is None:
        if app.config["ENV"] == "production":
            app.config.from_object(configmodule.Production)
        else:
            app.config.from_object(configmodule.Development)
    else:
        app.config.from_object(configmodule.Testing)

    initialize_extensions(app) # getting extensions ready for the work
    register_blueprint(app) # registering the blueprint for the app
    register_error_handler(app) # registering the error handler for the app

    return app


def initialize_extensions(app):
    db.init_app(app) # initializing  the database

    migrate.init_app(app, db)
    jwt.init_app(app)
    from app.model import Admin #, User

    # import database Model classes
    # callback function to load users.user_id when serializing the jwt identity
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    # callback function to load the user object when any protected route in accessed
    # this function takes user_id from the jwt and loads the user accordingly
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """
        ```
            # if in future versions there is two different types of authentication
            if jwt_data.get("user_type", 1) == 0:
                return Admin.query.filter_by(admin_id = identity).first()
            elif jwt_data.get("user_type") == 1:
                return User.query.get(identity)
        ```
        """
        identity = jwt_data["sub"]
        return Admin.query.get(identity)


def register_blueprint(app):

    #-----------------------------------------------------------------------------
    # registering the blueprint responsible for login/register and authentication and dashboard stuff
    #-----------------------------------------------------------------------------
    from app.web_app import web_app_blueprint
    app.register_blueprint(web_app_blueprint)
    # os.makedirs(name = os.path.join(app.root_path, user_blueprint.static_folder), exist_ok = True)

def register_error_handler(app):
    @app.errorhandler(500)
    def internal_error(e):
        logging.error(e)
        return jsonify(response = "Something went wrong!")
