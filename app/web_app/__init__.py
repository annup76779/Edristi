from flask import Blueprint

web_app_blueprint = Blueprint("web_app_blueprint", __name__, url_prefix="/api", static_folder = "../static")

from . import routes