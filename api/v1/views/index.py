#!/usr/bin/python3
"""my route is register in this index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.review import Review
from models.user import User
from models.place import Place
from models.amenity import Amenity


@app_views.route('/status')
def status():
    """status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns the number of objects by name"""
    classes = {
        City: "cities",
        State: "states",
        Amenity: "amenities",
        User: "users",
        Place: "places",
        Review: "reviews"
    }
    dictionary = {}
    for key, value in classes.items():
        count = storage.count(key)
        dictionary[value] = count
    return jsonify(dictionary)
