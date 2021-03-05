from flask_sqlalchemy import SQLAlchemy
from api.extensions import User
from flask import Flask
from typing import Dict, Any, List


class Alchemist:

    def __init__(self, db: SQLAlchemy, app: Flask):
        self.db = db
        self.app = app
        self.db.init_app(app)

    def get_users(self):
        data = []
        with self.app.app_context():
            users = self.db.session.query(User).all()
            for u in users:
                data.append(u.export())
        return data

    def get_user(self, username: str) -> Dict[str, Any]:
        data = {}
        with self.app.app_context():
            user = User.query.filter(User.username == username).all()
            data = user[0].export()
        return data