#!/usr/bin/python3
"""
This is a module that handls City objects
"""

from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def list_the_cities(state_id):
    """
    Retrieves the list of all the cities of a state
    """
    a_state = storage.get(State, state_id)
    if a_state is None:
        abort(404)
    cities_all = [city.to_dict() for city in a_state.cities]
    return jsonify(cities_all)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_the_city(city_id):
    """
    method for Retrieving a City object
    """
    a_city = storage.get(City, city_id)
    if a_city is None:
        abort(404)
    return jsonify(a_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_the_city(city_id):
    """
    method for Deleting a City object
    """
    a_city = storage.get(City, city_id)
    if a_city is None:
        abort(404)
    storage.delete(a_city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_the_city(state_id):
    """
    method for Creating a City
    """
    a_city = request.get_json(silent=True)
    if a_city is None:
        abort(400, 'Not a JSON')
    if not storage.get("State", str(state_id)):
        abort(404)
    if "name" not in a_city:
        abort(400, 'Missing name')
    a_city["state_id"] = state_id
    n_city = City(**a_city)
    n_city.save()
    rsp = jsonify(n_city.to_dict())
    rsp.status_code = 201
    return rsp


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_the_city(city_id):
    """
    method for Updating a City object
    """
    a_city = request.get_json(silent=True)
    if a_city is None:
        abort(400, 'Not a JSON')
    data = storage.get("City", str(city_id))
    if data is None:
        abort(404)
    for k, v in a_city.items():
        if k not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(data, k, v)
    data.save()
    return jsonify(data.to_dict())