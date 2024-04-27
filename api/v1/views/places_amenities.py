#!/usr/bin/python3
"""This module manage link between Place objects and Amenity objects"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities_get(place_id):
    """Methdo that retrieves the list of all Amenity objects of a Place"""
    place_ob = storage.get(Place, place_id)
    if place_ob is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities_ob = [amenity.to_dict() for amenity in place_ob.amenities]
    else:
        amenities_ob = [storage.get(Amenity, amenity_id).to_dict()
                        for amenity_id in place_ob.amenity_ids]
    return jsonify(amenities_ob)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_amenity_delete(place_id, amenity_id):
    """Method that reletes an Amenity object from a Place"""
    place_ob = storage.get(Place, place_id)
    if place_ob is None:
        abort(404)
    amenity_ob = storage.get(Amenity, amenity_id)
    if amenity_ob is None:
        abort(404)
    for element in place_ob.amenities:
        if element.id == amenity_ob.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                place_ob.amenities.remove(amenity_ob)
            else:
                place_ob.amenity_ids.remove(amenity_ob)
            storage.save()
            return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def place_amenity_post(place_id, amenity_id):
    """Method that links an Amenity object to a Place"""
    place_ob = storage.get(Place, place_id)
    if place_ob is None:
        abort(404)
    amenity_ob = storage.get(Amenity, amenity_id)
    if amenity_ob is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity_ob in place_ob.amenities:
            return (jsonify(amenity_ob.to_dict()), 200)
        place_ob.amenities.append(amenity_ob)
    else:
        if amenity_id in place_ob.amenity_ids:
            return (jsonify(amenity_ob.to_dict()), 200)
        place_ob.amenity_ids.append(amenity_id)

    storage.save()
    return (jsonify(amenity_ob.to_dict()), 201)
