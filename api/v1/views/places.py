#!/usr/bin/python3

from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def all_places(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if (request.method == 'GET'):
        places = storage.all(places).values()
        list_places = [place.to_dict()
                       for place in places if place.city_id == city_id]
        return jsonify(list_places)
    if (request.method == 'POT'):
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify("Not a JSON"), 400
        if 'user_id' not in json_data.keys():
            return jsonify("Missing user_id"), 400
        user = storage.get(User, json_data['user_id'])
        if not user:
            abort(404)
        if 'name' not in json_data.keys():
            return jsonify("Missing name"), 400
        place = Place(**json_data)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if (request.method == 'GET'):
        return jsonify(place.to_dit())
    if (request.method == 'DELETE'):
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if (request.method == 'PUT'):
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify('Not a JSON'), 400
        key_to_ignore = ['id',
                         'user_id',
                         'city_id',
                         'created_at',
                         'updated_at']
        for key, value in json_data.items():
            if key not in key_to_ignore:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
