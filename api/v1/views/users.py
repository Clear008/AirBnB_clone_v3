#!/usr/bin/python3
"""
This is a module that handls User objects
"""
from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_the_users(user_id):
    """
    Method for Retrieving all Users object
    """
    if user_id:
        a_user = storage.get(User, user_id)
        if a_user is None:
            abort(404)
        return jsonify(a_user.to_dict())
    else:
        users_list = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users_list)


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

    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


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

    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(a_user, k, v)

    storage.save()
    return jsonify(a_user.to_dict()), 200
