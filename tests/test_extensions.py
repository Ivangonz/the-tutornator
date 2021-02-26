import os
import sqlite3

import pytest
import random

from api.app import app, db
from api.extensions import User, Role

usernames = [
    "apple", "banana", "cherry", "dragon fruit", "egg fruit", "Farkleberry", "grapefruit",
    "honeydewmelon", "Indonesian Lime", "Jackfruit"
]
emails = [
    'a@a.com', 'b@b.com', 'c@c.com', 'd@d.com', 'e@e.com', 'f@f.com', 'g@g.com', 'h@h.com',
    'i@i.com', 'j@j.com'
]
first_names = [
    'Bob', 'Chad', 'Spok', 'Elmo', 'Twee', 'Dee', 'Ainz', 'ConAir', 'Winston', 'Who'
]
last_names = [
    'Whitaker', 'Bolton', 'Vang', 'Mosley', 'Faulkner', 'Kline', 'Farmer', 'Short',
    'Huerta', 'Osborn'
]
passwords = [
    'password', 'asdf', '1qaz!QAZ2wsx@WSX', 'abcd1234', 'ConnerWithAnEIsGreat',
    'ConnorWithAnOIsBronzeLeague', 'Woooooooooooo', 'ThisIsMyPasswordForADatabase',
    'TutornatorTutornatorTutornator', 'Alexisasmartypants'
]


def test_create_users():
    db.init_app(app)
    print("Generating test users...")
    with app.app_context():
        for i in range(10):
            user = User(email=emails[i], firstname=first_names[i], lastname=last_names[i], username=usernames[i])
            user.hash_password(passwords[i])
            user.roles.append(Role(name='tutor'))
            db.session.add(user)
            db.session.commit()


def test_query_users():
    db.init_app(app)
    with app.app_context():
        print(db.session.query(User).all())


def test_delete_users():
    db.init_app(app)
    print("Cleaning up test users...")
    with app.app_context():
        for i in range(10):
            User.query.filter_by(username=usernames[i]).delete()
            db.session.commit()
