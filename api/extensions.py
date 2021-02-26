import os
import time
from dataclasses import dataclass

import jwt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from api.constants import SECRET_KEY
from api.utils import encode_img

db = SQLAlchemy()
img_path = os.path.abspath('images/default-avatar.png')

@dataclass
class User(db.Model):
    __tablename__ = 'users'

    username: str
    email: str
    firstname: str
    lastname: str
    roles: str
    classes: str
    languages: str
    biography: str
    avatar: bytes

    # SQLAlchemy will automatically set the first Integer PK column that's not marked as a FK as autoincrement=True.
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
    biography = db.Column(db.String(8000), server_default='')
    avatar = db.Column(db.BLOB(), server_default=encode_img(img_path))


    # Define the relationship to outer tables via a bridge table
    roles = db.relationship('Role', secondary='user_roles')
    classes = db.relationship('Class', secondary='user_classes')
    languages = db.relationship('Language', secondary='user_languages')

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
        except Exception as e:
            print(e)
            return
        return User.query.get(data['id'])


# Define the Role data-model
@dataclass
class Role(db.Model):
    __tablename__ = 'roles'
    name: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the Class data-model
@dataclass
class Class(db.Model):
    __tablename__ = 'classes'
    name: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserClasses association table
class UserClasses(db.Model):
    __tablename__ = 'user_classes'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    class_id = db.Column(db.Integer(), db.ForeignKey('classes.id', ondelete='CASCADE'))


# Define the Language data-model
@dataclass
class Language(db.Model):
    __tablename__ = 'languages'
    name: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserLanguages association table
class UserLanguages(db.Model):
    __tablename__ = 'user_languages'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    languages_id = db.Column(
        db.Integer(), db.ForeignKey('languages.id', ondelete='CASCADE')
    )
