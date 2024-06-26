#!/usr/bin/python3
"""
This is a module that handls User objects
"""
from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """Retrieves the list of all User """
    value = storage.all(User).values()
    users_list = [user.to_dict() for user in value]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    if storage.get(User, user_id) is None:
        abort(404)
    return jsonify(storage.get(User, user_id).to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_the_user(user_id):
    """
    Method for Deleting a User object
    """
    a_user = storage.get(User, user_id)
    if a_user is None:
        abort(404)
    storage.delete(a_user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    Method for Creating a User object
    """
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json(silent=True):
        abort(400, 'Missing email')
    if 'password' not in request.get_json(silent=True):
        abort(400, 'Missing password')

    n_user = User(**request.get_json())
    storage.new(n_user)
    storage.save()
    return (jsonify(n_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Method for Updating a User object
    """
    a_user = storage.get(User, user_id)
    if not a_user:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(a_user, k, v)

    storage.save()
    return jsonify(a_user.to_dict()), 200
