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
    a_state = storage.get(State, state_id)
    if a_state is None:
        abort(404)

    city_data = request.get_json(silent=True)
    if city_data is None:
        abort(400, 'Not a JSON')
    if "name" not in city_data:
        abort(400, 'Missing name')

    city_data["state_id"] = state_id
    new_city = City(**city_data)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_the_city(city_id):
    """
    method for Updating a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city_data = request.get_json(silent=True)
    if city_data is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in city_data.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200
