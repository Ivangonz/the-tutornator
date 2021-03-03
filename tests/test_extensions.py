import os
import sqlite3

import pytest
import random

from api.app import app, db
from api.extensions import User, Role, Course
from api.utils import encode_img

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

biography="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec massa nibh, interdum at massa vitae, euismod scelerisque sem. Curabitur malesuada nisi cursus, imperdiet augue ut, dapibus dolor. Pellentesque iaculis libero ipsum, in facilisis purus gravida et. Cras non rhoncus lacus, eu accumsan leo." \
          " \nFusce consequat lacus et orci vestibulum, id cursus dui eleifend. Nam vehicula tincidunt ante, vel tincidunt libero luctus ac. Suspendisse auctor dui nunc, vel auctor nibh pellentesque vitae. Nulla turpis purus, suscipit eget odio non, condimentum suscipit justo. Curabitur id semper orci."

avatar = encode_img('api/images/default-avatar.png')

roles = [{"admin", "tutor"}, "admin", "tutor", "tutor", "tutor", "tutor", "tutor", "tutor",
         "tutor", "tutor"]

courses = [["CS-1010", "CS1030", "CS-1400", "CS-1410"],
           ["CS-1010", "CS1030", "CS-1400", "CS-1410", "CS-2130", "CS2350"],
           ["CS-1010", "CS1030", "CS-1400", "CS-1410", "CS-2130", "CS2350"],
           ["CS-1010", "CS1030", "CS-1400", "CS-1410", "CS-2130", "CS2350"],
           [
               "CS-1010", "CS1030", "CS-1400", "CS-1410", "CS-2130", "CS2350", "CS2420",
               "CS2450", "CS2550", "CS2705"
           ],
           [
               "CS-1010", "CS1030", "CS-1400", "CS-1410", "CS-2130", "CS2350", "CS2420",
               "CS2450", "CS2550", "CS2705"
           ],
           [
               "CS-1010", "CS1030", "CS-1400", "CS-1410", "CS-2130", "CS2350", "CS2420",
               "CS2450", "CS2550", "CS2705", "CS-2810", "CS3280"
           ],
           [
               "CS-1010", "CS1030", "CS-1400", "CS-1410", "CS-2130", "CS2350", "CS2420",
               "CS2450", "CS2550", "CS2705", "CS-2810", "CS3280"
           ], {"CS2350", "CS2420", "CS2450", "CS2550", "CS2705", "CS-2810", "CS3280"},
           [
               "CS2350", "CS2420", "CS2450", "CS2550", "CS2705", "CS-2810", "CS3280",
               "CS-3550", "CS-4110"
           ]]

languages = [["Assembly", "C#", "C++"], ["CSS", "HTML", "JavaScript"], ["Java", "SQL"],
             ["Assembly", "C#", "C++", "SQL"],
             ["CSS", "HTML", "JavaScript", "Assembly", "C#", "C++"],
             ["CSS", "HTML", "JavaScript", "Assembly", "C#", "C++"],
             ["CSS", "HTML", "JavaScript", "Java", "SQL"],
             ["Java", "SQL", "Assembly", "C#", "C++"],
             ["Assembly", "C#", "C++", "CSS", "HTML", "JavaScript", "Java", "SQL"],
             ["Assembly", "C#", "C++", "CSS", "HTML", "JavaScript", "Java", "SQL"]]

# schedules=[{{1, }{}},
# {}]
# (time_day int, time_start time, time_end time)


def test_create_users():
    db.init_app(app)
    print("Generating test users...")
    with app.app_context():
        all_courses = db.session.query(Course).all()

        for i in range(10):
            user = User(
                email=emails[i],
                firstname=first_names[i],
                lastname=last_names[i],
                username=usernames[i]
            )
            user.hash_password(passwords[i])
            for j in range(len(courses[i])):
                course = Course(
                    name=courses[i][j]
                )
                if courses[i][j] in all_courses:
                    course.usercourses.append(user)
                else:
                    user.courses.append(Course(name=courses[i][j]))

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
