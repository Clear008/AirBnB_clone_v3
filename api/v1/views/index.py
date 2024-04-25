#!/usr/bin/python3
'''The index view for the API.'''

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the current response of the API."""
    return jsonify({"status": "OK"})