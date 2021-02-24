from flask import Blueprint, abort, g, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth

from api.extensions import Role, User, db

auth_views = Blueprint('auth_views', __name__)
auth = HTTPBasicAuth()


@auth_views.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token, 'duration': 600})


@auth_views.route('/api/account')
@auth.login_required
def get_account():
    return jsonify({
        'username': g.user.username,
        'email': g.user.email,
        'firstname': g.user.firstname,
        'lastname': g.user.lastname,
        'roles': g.user.roles,
        'password_hash': g.user.password_hash
    })


@auth_views.route('/api/profile', methods=['PUT'])
@auth.login_required
def profile():
    user_obj = User.query.filter(User.username == g.user.username).first()
    user_obj.firstname = request.json.get('firstname')
    user_obj.lastname = request.json.get('lastname')
    db.session.add(user_obj)
    db.session.commit()
    return jsonify({
        'username': g.user.username,
        'email': g.user.email,
        'firstname': g.user.firstname,
        'lastname': g.user.lastname,
        'roles': g.user.roles
    })


@auth_views.route('/api/admin/users')
@auth.login_required(role='admin')
@auth.login_required
def user_list():
    users = User.query.all()
    return jsonify(users)


@auth_views.route('/api/admin/roles')
@auth.login_required(role='admin')
@auth.login_required
def roles_list():
    roles = Role.query.all()
    return jsonify(roles)


# Update, Create, Delete User


@auth_views.route('/api/admin/user/<id>', methods=['PUT'])
@auth.login_required(role='admin')
@auth.login_required
def update_user(id):
    user_obj = User.query.filter(User.id == id).first()
    user_obj.firstname = request.json.get('firstname')
    user_obj.lastname = request.json.get('lastname')
    user_obj.username = request.json.get('username')

    # roles
    user_obj.roles[:] = []
    roles_json = request.json.get('roles')
    for role in roles_json:
        role_obj = Role.query.filter(Role.id == role['id']).first()
        user_obj.roles.append(role_obj)

    try:
        user_obj.hash_password(request.json.get('password'))
    except Exception as e:
        print("Password param was not passed in json.  So not updating it", e)
    db.session.add(user_obj)
    db.session.commit()
    return jsonify({'operation': 'success'})


@auth_views.route('/api/admin/user', methods=['POST'])
@auth.login_required(role='admin')
@auth.login_required
def create_user():
    print('creating user')
    username = request.json.get('username')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username, firstname=firstname, lastname=lastname, email=email)
    user.hash_password(password)

    roles_json = request.json.get('roles')
    for role in roles_json:
        role_obj = Role.query.filter(Role.id == role['id']).first()
        user.roles.append(role_obj)

    db.session.add(user)
    db.session.commit()
    return jsonify({'operation': 'success'})


@auth_views.route('/api/admin/user/<id>', methods=['DELETE'])
@auth.login_required(role='admin')
@auth.login_required
def delete_user(id):
    print('deleting user', id)
    user_obj = User.query.filter(User.id == id).first()
    db.session.delete(user_obj)
    db.session.commit()
    return jsonify({'operation': 'success'})


# Update, Create, Delete Role


@auth_views.route('/api/admin/role/<id>', methods=['PUT'])
@auth.login_required(role='admin')
@auth.login_required
def update_role(id):
    print('updating role', id)
    role_obj = Role.query.filter(Role.id == id).first()
    role_obj.name = request.json.get('name')
    db.session.add(role_obj)
    db.session.commit()
    return jsonify({'operation': 'success'})


@auth_views.route('/api/admin/role', methods=['POST'])
@auth.login_required(role='admin')
@auth.login_required
def create_role():
    print('creating role')
    name = request.json.get('name')
    role = Role(name=name)

    db.session.add(role)
    db.session.commit()
    return jsonify({'operation': 'success'})


@auth_views.route('/api/admin/role/<id>', methods=['DELETE'])
@auth.login_required(role='admin')
@auth.login_required
def delete_role(id):
    print('deleting role', id)
    role_obj = Role.query.filter(Role.id == id).first()
    db.session.delete(role_obj)
    db.session.commit()
    return jsonify({'operation': 'success'})


# AUTH UTILITY CLASSES (NOT VIEWS, BUT USED BY VIEWS)


# See https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# search on 401 replacing with 403
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# below needed for role based auth like:
# @auth.login_required(role='admin')
# or
# @auth.login_required(role=['admin', 'member'])
# see https://flask-httpauth.readthedocs.io/en/latest/
@auth.get_user_roles
def get_user_roles(user):
    sql_statement = "SELECT roles.name FROM roles JOIN user_roles ON roles.id=user_roles.role_id JOIN users ON users.id=user_roles.user_id WHERE users.username='" + g.user.username + "'"
    lt = db.engine.execute(sql_statement)
    # converts tuple list to list:
    tuple_to_list = [item for t in lt for item in t]
    return tuple_to_list
