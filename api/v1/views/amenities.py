#!/usr/bin/python3
"""create aminities route"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import request, jsonify, abort


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def all_amenities():
    """return all amenities"""
    if (request.method == 'GET'):
        amenities = storage.all(Amenity).values()
        list_amenities = [amenity.to_dict() for amenity in amenities]
        return jsonify(list_amenities), 200
    if (request.method == 'POST'):
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify("Not a JSON"), 400
        if 'name' not in json_data.keys():
            return jsonify("Missing name"), 400
        amenity = Amenity(**json_data)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """ manage amenity id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if (request.method == 'GET'):
        return jsonify(amenity.to_dict()), 200
    if (request.method == 'DELETE'):
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if (request.method == 'PUT'):
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify('Not a JSON'), 400
        for key in ['id', 'created_at', 'updated_at']:
            json_data.pop(key, None)
        for key, value in json_data.items():
            setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity), 200
