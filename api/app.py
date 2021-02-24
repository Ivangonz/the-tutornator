#!/usr/bin/env python
import os

from flask import Flask
from flask_cors import CORS

from api.constants import SECRET_KEY, SQL_ALCHEMY_DATABASE_URI
from api.extensions import db
from api.utils import create_test_admin
from api.views.authviews import auth_views


def create_app():
    flask_app = Flask(__name__)
    CORS(flask_app)

    flask_app.register_blueprint(auth_views)
    # flask_app.register_blueprint(db_views)

    flask_app.config['SECRET_KEY'] = SECRET_KEY
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = SQL_ALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()
        create_test_admin()

    return flask_app


app = create_app()

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)
