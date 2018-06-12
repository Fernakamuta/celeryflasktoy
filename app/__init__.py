from flask import Flask
from .survey import bp_survey


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_survey)
    return app
