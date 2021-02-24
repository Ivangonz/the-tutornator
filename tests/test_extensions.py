import pytest
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
    'password', 'asdf', '1qaz!QAZ2wsx@WSX', 'abcd1234', 'ConnorWithAnEIsLame', 'ConnorWithAnOIsCooler', 'Woooooooooooo',
    'Short', 'Huerta', 'Osborn'
]


@pytest.mark.parametrize('email, firstname, lastname, username, passwords', [usernames, emails, first_names, last_names, passwords])
def test_create_users(email, firstname, lastname, username):
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(
            email=email,
            firstname=firstname,
            lastname=lastname,
            username=username
        )
        user.hash_password('blue')
        user.roles.append(Role(name='member'))
        db.session.add(user)
        db.session.commit()
