#!/usr/bin/env python
import os
import time
from flask import Flask, abort, request, jsonify, g, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response
from functools import wraps
from flask_cors import CORS, cross_origin
from dataclasses import dataclass

# initialization
app = Flask(__name__)

# the below should make all routes cross origin enabled
# see: https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
CORS(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


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
                          app.config['SECRET_KEY'],
                          algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
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


db.create_all()

# Create 'member@example.com' user with no roles
if not User.query.filter(User.email == 'member@example.com').first():
    user = User(
        email='member@example.com', firstname='Momo', lastname='Man', username='momoman'
    )
    user.hash_password('blue')
    user.roles.append(Role(name='member'))
    db.session.add(user)
    db.session.commit()

# Create 'admin@example.com' user with 'Admin' and 'Agent' roles
if not User.query.filter(User.email == 'lfernandez@weber.edu').first():
    user = User(
        email='lfernandez@weber.edu',
        firstname='Luke',
        lastname='Fern',
        username='lfernandez'
    )
    user.hash_password('white')
    user.roles.append(Role(name='admin'))
    user.roles.append(Role(name='agent'))
    db.session.add(user)
    db.session.commit()

############################################ROUTES ROUTES ROUTES ROUTES##########################################
import authviews


# a sample route
@app.route("/greeting")
def greeting():
    print(request.headers)
    return {'greeting': request.headers['Authorization']}


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)
