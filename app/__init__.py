from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()


from config import config
from .main import main_blueprint
from .api import api
from .oauth import oauth


blueprints=[
    (main_blueprint,''),
    (api,'/api'),
    (oauth,'/oauth')
]


def create_app():
    app=Flask(__name__)
    app.config.from_object(config['default'])

    db.init_app(app)

    init_blueprint(app, blueprints)

    return app


def init_blueprint(app,blue_prints):
    for item in blue_prints:
        app.register_blueprint(item[0],url_prefix=item[1])