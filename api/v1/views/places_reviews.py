#!/usr/bin/python3
"""
This is a module that handls  Review objects
"""

from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
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
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Method for Creating a Review
    """
    if storage.get("Place", str(place_id)) is None:
        abort(404)

    dt = request.get_json(silent=True)
    if dt is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in dt:
        abort(400, 'Missing user_id')
    if 'text' not in dt:
        abort(400, 'Missing text')

    if storage.get("User", str(dt['user_id'])) is None:
        abort(404)

    n_review = Review(place_id=place_id, **dt)
    storage.new(n_review)
    storage.save()

    return jsonify(n_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Method for Updating a Review object
    """
    if storage.get(Review, review_id) is None:
        abort(404)

    dt = request.get_json(silent=True)
    if dt is None:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in dt.items():
        if key not in ignore_keys:
            setattr(storage.get(Review, review_id).to_dict(), key, value)

    storage.save()
    return jsonify(storage.get(Review, review_id).to_dict()), 200
