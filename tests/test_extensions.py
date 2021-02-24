import os
import sqlite3

import pytest
import random

from api.extensions import Role, User, db


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
    for i in range(10):
        if not User.query.filter(User.email == 'member@example.com').first():
            user = User(email=emails[i], firstname=first_names[i], lastname=last_names[i], username=usernames[i])
            user.hash_password(passwords[i])
            user.roles.append(Role(name='member'))
            db.session.add(user)
            db.session.commit()

