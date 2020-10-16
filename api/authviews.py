from app import app
from app import auth
from app import User, Role, g, db
from flask import Flask, abort, request, jsonify, url_for, render_template, make_response
import copy
import json


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@app.route('/api/account')
@auth.login_required
def get_account():
    return jsonify({ \
        'username': g.user.username, \
        'email': g.user.email, \
        'firstname': g.user.firstname, 'lastname': g.user.lastname, \
        'roles': g.user.roles
    }) 


@app.route('/api/profile', methods=['PUT'])
@auth.login_required
def profile():
    userObj = User.query.filter(User.username == g.user.username).first()
    userObj.firstname = request.json.get('firstname')
    userObj.lastname = request.json.get('lastname')
    db.session.add(userObj)
    db.session.commit()
    return jsonify({ \
        'username': g.user.username, \
        'email': g.user.email, \
        'firstname': g.user.firstname, 'lastname': g.user.lastname, \
        'roles': g.user.roles
    })

@app.route('/api/admin/users')
@auth.login_required(role='admin')
@auth.login_required
def user_list():
    users = User.query.all()
    return jsonify(users)

@app.route('/api/admin/roles')
@auth.login_required(role='admin')
@auth.login_required
def roles_list():
    roles = Role.query.all()
    return jsonify(roles)

################## Update, Create, Delete User ########################

@app.route('/api/admin/user', methods=['PUT'])
@auth.login_required(role='admin')
@auth.login_required
def updateUser():
    print('updating user', request.json.get('id'))
    userObj = User.query.filter(User.id == request.json.get('id')).first()
    print(userObj)
    print('XXXXXXXXXXXXX')
    print(request.json.get('roles'))
    userObj.firstname = request.json.get('firstname')
    userObj.lastname = request.json.get('lastname')
    userObj.username = request.json.get('username')

    # roles
    userObj.roles[:] = []
    rolesJSON = request.json.get('roles')
    for role in rolesJSON:
        roleObj = Role.query.filter(Role.id == role['id']).first()
        userObj.roles.append(roleObj)

    try:
        userObj.hash_password(request.json.get('password'))
    except:
        print("Password param was not passed in json.  So not updating it")    
    db.session.add(userObj)
    db.session.commit()
    return jsonify({'operation': 'success'})


@app.route('/api/admin/user', methods=['POST'])
@auth.login_required(role='admin')
@auth.login_required
def createUser():
    print('creating user')
    username = request.json.get('username')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username,firstname=firstname,lastname=lastname,email=email)
    user.hash_password(password)
    
    rolesJSON = request.json.get('roles')
    for role in rolesJSON:
        roleObj = Role.query.filter(Role.id == role['id']).first()
        user.roles.append(roleObj)

    db.session.add(user)
    db.session.commit()
    return jsonify({'operation': 'success'})

@app.route('/api/admin/user', methods=['DELETE'])
@auth.login_required(role='admin')
@auth.login_required
def deleteUser():
    print('deleting userx', request.json.get('id'))
    userObj = User.query.filter(User.id == request.json.get('id')).first()
    db.session.delete(userObj)
    db.session.commit()
    return jsonify({'operation': 'success'})

################## Update, Create, Delete Role ########################

@app.route('/api/admin/role', methods=['PUT'])
@auth.login_required(role='admin')
@auth.login_required
def updateRole():
    print('updating role', request.json.get('id'))
    roleObj = Role.query.filter(Role.id == request.json.get('id')).first()
    roleObj.name = request.json.get('name')
    db.session.add(roleObj)
    db.session.commit()
    return jsonify({'operation': 'success'})


@app.route('/api/admin/role', methods=['POST'])
@auth.login_required(role='admin')
@auth.login_required
def createRole():
    print('creating role')
    name = request.json.get('name')
    role = Role(name=name)
    
    db.session.add(role)
    db.session.commit()
    return jsonify({'operation': 'success'})

@app.route('/api/admin/role', methods=['DELETE'])
@auth.login_required(role='admin')
@auth.login_required
def deleteRole():
    print('deleting role', request.json.get('id'))
    roleObj = Role.query.filter(Role.id == request.json.get('id')).first()
    db.session.delete(roleObj)
    db.session.commit()
    return jsonify({'operation': 'success'})



#########################AUTH UTILITY CLASSES (NOT VIEWS, BUT USED BY VIEWS)#################################

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
    sqlStatement = "SELECT roles.name FROM roles JOIN user_roles ON roles.id=user_roles.role_id JOIN users ON users.id=user_roles.user_id WHERE users.username='" + g.user.username + "'"
    lt = db.engine.execute(sqlStatement)
    # converts tuple list to list:
    tupleToList = [item for t in lt for item in t] 
    return tupleToList

################################################################

"""




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    firstname = request.json.get('password')
    lastname = request.json.get('lastname')

    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user = User(username=username,firstname=firstname,lastname=lastname,email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})



@app.route('/api/resource')
# @auth.login_required(role='admin')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})






@app.route('/api/testrole')
# @auth.login_required(role='agent')
@auth.login_required(role=['admin', 'agent'])
def api_demo():
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbxxxxx')
    print(g.user.username)
    return jsonify({'username': 'foobars'})

# see https://flask-httpauth.readthedocs.io/en/latest/
@auth.get_user_roles
def get_user_roles(user):
    print('in get_user_roles')
    print(user.username)
    print(auth.current_user())
    print(g.user.username)
    sqlStatement = "SELECT roles.name FROM roles JOIN user_roles ON roles.id=user_roles.role_id JOIN users ON users.id=user_roles.user_id WHERE users.username='" + g.user.username + "'"
    lt = db.engine.execute(sqlStatement)
    # converts tuple list to list:
    tupleToList = [item for t in lt for item in t] 
    # print(roleName)
    # roleName = [row for row in roleName]

    # print(roleName)
    # return ['admin']
    # return user.get_roles()
    return tupleToList



@app.route('/api/any')
@auth.login_required()
def api_role():
    return jsonify({'username': g.user.username, 'role': 'any'})

@app.route('/api/admin')
@auth.login_required(role='admin')
def api_role_a():
    return jsonify({'username': g.user.username, 'role': 'admin'})

@app.route('/api/member')
@auth.login_required(role='member')
def api_role_c():
    return jsonify({'username': g.user.username, 'role': 'member'})  

@app.route('/api/admin_member')
@auth.login_required(role=['admin', 'member'])
def api_role_b():
    return jsonify({'username': g.user.username, 'role': 'admin_member'})  

"""
