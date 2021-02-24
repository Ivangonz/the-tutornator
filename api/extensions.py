import time
from dataclasses import dataclass

import jwt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from api.constants import SECRET_KEY

db = SQLAlchemy()


@dataclass
class User(db.Model):
    __tablename__ = 'users'

    id: int
    username: str
    # password_hash: str (we leave this out for security reasons so as not to return it to the browser)
    email: str
    firstname: str
    lastname: str
    roles: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    firstname = db.Column(
        db.String(100, collation='NOCASE'), nullable=False, server_default=''
    )
    lastname = db.Column(
        db.String(100, collation='NOCASE'), nullable=False, server_default=''
    )

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode({
            'id': self.id,
            'exp': time.time() + expires_in
        },
                          SECRET_KEY,
                          algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])


# Define the Role data-model
@dataclass
class Role(db.Model):
    __tablename__ = 'roles'
    id: int
    name: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


#
# db.create_all()
#
# Create 'member@example.com' user with no roles