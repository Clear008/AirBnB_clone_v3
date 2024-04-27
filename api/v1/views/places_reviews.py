#!/usr/bin/python3
"""
This is a module that handls  Review objects
"""

from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Method that retrieves the list of all Review of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review).values()
    all_reviews = [review.to_dict()
                   for review in reviews if review.place_id == place_id]
    return jsonify(all_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_the_review(review_id):
    """Method that Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_the_review(review_id):
    """
    Method for Deleting a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Method for Creating a Review
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    dt = request.get_json(silent=True)
    if dt is None:
        return jsonify("Not a JSON"), 400
    if 'user_id' not in dt:
        return jsonify("Missing user_id"), 400
    if 'text' not in dt:
        return jsonify("Missing text"), 400

    user = storage.get(User, dt['user_id'])
    if user is None:
        abort(404)
    dt['place_id'] = place_id
    n_review = Review(**dt)
    storage.new(n_review)
    storage.save()

    return jsonify(n_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Method for Updating a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    dt = request.get_json(silent=True)
    if dt is None:
        return jsonify("Not a JSON"), 400

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in dt.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
