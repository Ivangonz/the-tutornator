import os
import time
from dataclasses import dataclass

import jwt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from api.constants import SECRET_KEY
from api.utils import encode_img

db = SQLAlchemy()
img_path = os.path.abspath('api/images/default-avatar.png')


def create_test_admin():
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


@dataclass
class User(db.Model):
    __tablename__ = 'users'

    username: str
    email: str
    firstname: str
    lastname: str
    biography: str = ''
    avatar: bytes = encode_img(img_path)
    roles: str = ''
    courses: str = ''
    languages: str = ''

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
    avatar = db.Column(db.BLOB())

    # Define the relationship to outer tables via a bridge table
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('userroles', lazy='dynamic'))
    courses = db.relationship('Course', secondary='user_courses', backref=db.backref('usercourses', lazy='dynamic'))
    languages = db.relationship('Language', secondary='user_languages', backref=db.backref('userlanguages', lazy='dynamic'))
    schedules = db.relationship("Schedule", backref='users', cascade='all')

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
class Course(db.Model):
    __tablename__ = 'courses'
    name: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserClasses association table
class UserCourses(db.Model):
    __tablename__ = 'user_courses'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id', ondelete='CASCADE'))


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


# Define the Schedule data-model
@dataclass
class Schedule(db.Model):
    __tablename__ = 'Schedules'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    time_day = db.Column(db.Integer())
    time_start = db.Column(db.Time())
    time_end = db.Column(db.Time())
