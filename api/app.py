#!/usr/bin/env python
import os
from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from api.extensions import db

app = Flask(__name__)

CORS(app)


def create_app():
    flask_app = Flask(__name__)
    CORS(flask_app)

    flask_app.register_blueprint(auth_views)
    flask_app.register_blueprint(db_views)

    # TODO: Need to change some of these to environment variables.
    flask_app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    flask_app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()

    return flask_app


app = create_app()


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)
