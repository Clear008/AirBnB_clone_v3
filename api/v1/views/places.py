#!/usr/bin/python3
"""create a places view """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
def places_by_city(city_id):
    """get places by city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if (request.method == 'GET'):
        places = storage.all(Place).values()
        list_of_places = [place.to_dict()
                          for place in places if place.city_id == city_id]
        return jsonify(list_of_places)
    if (request.method == 'POST'):
        data = request.get_json(silent=True)
        if not data:
            return jsonify("Not a JSON"), 400
        if "user_id" not in data.keys():
            return jsonify("Missing user_id"), 400
        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)
        if "name" not in data.keys():
            return jsonify("Missing name"), 400
        data['city_id'] = city_id
        place = Place(**data)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
def places(place_id):
    """place by her place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if (request.method == 'GET'):
        return jsonify(place.to_dict())
    if (request.method == 'DELETE'):
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if (request.method == 'PUT'):
        data = request.get_json(silent=True)
        if not data:
            return jsonify("Not a JSON"), 400
        key_to_ignore = ["id",
                         "user_id",
                         "city_id",
                         "created_at",
                         "updated_at"]
        for key, value in data.items():
            if key not in key_to_ignore:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
