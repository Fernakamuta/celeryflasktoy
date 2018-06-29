from pathlib import Path

from flask import Flask
from .views import bp_survey


def config_path(mode):
    return Path(__file__).parents[1].joinpath('config', f'{mode}.py')


def create_app(mode='dev'):
    filepath = config_path(mode)

    app = Flask(__name__)
    app.config.from_pyfile(filepath)
    app.register_blueprint(bp_survey)
    return app
