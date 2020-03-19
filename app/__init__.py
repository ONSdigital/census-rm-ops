import os

from flask import Flask
from flask_assets import Environment

from app.views import setup_blueprints


def create_app(config_name=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    assets = Environment(app)
    assets.init_app(app)
    config_name = config_name or os.getenv("APP_SETTINGS", "Config")
    app_config = f'config.{config_name}'
    app.config.from_object(app_config)
    setup_blueprints(app)
    return app
