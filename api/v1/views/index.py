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
    """Returns Json response"""
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
    list_of_counts = {}
    for key in classes.keys():
        count = storage.count(key.__name__)
        if key.__name__ == City:
            list_of_counts["cities"] = count
        if key.__name__ == State:
            list_of_counts["states"] = count
        if key.__name__ == Amenity:
            list_of_counts["amenities"] = count
        if key.__name__ == User:
            list_of_counts["places"] = count
        if key.__name__ == Review:
            list_of_counts["reviews"] = count
    return jsonify(list_of_counts)
        
