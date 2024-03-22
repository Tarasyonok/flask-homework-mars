import flask
from flask import request, jsonify, make_response, redirect

from . import db_session
from .users import User

blueprint = flask.Blueprint('user_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return flask.jsonify(
        {'users': [str(item.to_dict()) for item in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    print(user_id)
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'user': user.to_dict()})


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    required_columns = ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in required_columns):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()

    kwargs = {}
    for key in required_columns[:-1]:
        kwargs[key] = request.json[key]
    print(kwargs)

    user = User(**kwargs)
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return make_response(jsonify({'success': 'OK'}))


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    required_columns = ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in required_columns):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()

    user = db_sess.query(User).get(user_id)

    if not user:
        return make_response(jsonify({'error': 'Bad request'}), 400)

    print(user)

    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']

    user.set_password(request.json['password'])

    db_sess.commit()
    return make_response(jsonify({'id': user.id}))