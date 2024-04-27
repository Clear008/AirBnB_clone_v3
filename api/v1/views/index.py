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
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    classes = {"amenities": Amenity,  "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    dictionary_count = {}
    for key, value in classes.items():
        dictionary_count[key] = storage.count(value)
    return jsonify(dictionary_count)

