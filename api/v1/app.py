#!/usr/bin/python3
"""run the app with style"""


from os import getenv
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """404 error with json"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """close the storage"""
    storage.close()


if __name__ == "__main__":
    my_host = getenv("HBNB_API_HOST", "0.0.0.0")
    my_port = getenv("HBNB_API_PORT", "5000")
    app.run(host=my_host, port=my_port, threaded=True)
