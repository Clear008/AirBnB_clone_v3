#!/usr/bin/python3
"""Start Api connection"""

from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    ''' handles 404 error with json '''
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.teardown_appcontext
def teardown_db(exception):
    """close the session after each request """
    storage.close()


if __name__ == "__main__":
    my_host = getenv('HBNB_API_HOST')
    my_port = getenv('HBNB_API_PORT')
    app.run(host=my_host, port=my_port, threaded=True)
