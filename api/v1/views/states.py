#!/usr/bin/python3
"""state route"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, jsonify, abort


@app_views.route('/states',
                 methods=['GET', 'PUT', 'POST', 'DELETE'],
                 strict_slashes=False)
def all_states():
    """return all State"""
    if (request.method == 'GET'):
        states = storage.all(State).values()
        list_of_states = [state.to_dict() for state in states]
        return jsonify(list_of_states)
    if (request.method == 'POST'):
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify("Not a JSON"), 400
        if 'name' not in json_data.keys():
            return jsonify("Missing name"), 400
        state = State(**json_data)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'POST', 'DELETE'],
                 strict_slashes=False)
def state_id(state_id):
    """return the state with theid"""
    the_state = storage.get(State, state_id)
    if not the_state:
        abort(404)
    if (request.method == 'GET'):
        return jsonify(the_state.to_dict()), 200
    if (request.method == 'DELETE'):
        storage.delete(the_state)
        storage.save()
        return jsonify({}), 200
    if (request.method == 'PUT'):
        the_state = storage.get(State, state_id)
        if not the_state:
            abort(404)
        data = request.get_json(silent=True)
        if not data:
            return jsonify("Not a JSON"), 400
        keys_to_ignore = ["id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in keys_to_ignore:
                setattr(the_state, key, value)
        storage.save()
        return jsonify(the_state.to_dict()), 200
