#!/usr/bin/python3
"""
This is a module that handls  Review objects
"""

from flask import jsonify,  abort, request
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_the_reviews(place_id=None, review_id=None):
    """
    Method for Retrieving the list of all Review objects
    """
    if review_id:
        a_review = storage.get(Review, review_id)
        if a_review is None:
            abort(404)
        return jsonify(a_review.to_dict())
    elif place_id:
        a_place = storage.get("Place", str(place_id))
        if a_place is None:
            abort(404)
        reviews = [a_review.to_dict() for a_review in a_place.reviews]
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_the_review(review_id):
    """
    Method for Deleting a Review object
    """
    if storage.get(Review, review_id) is None:
        abort(404)
    storage.delete(storage.get(Review, review_id))
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

    for k, v in dt.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(storage.get(Review, review_id), k, v)

    storage.save()
    return jsonify(storage.get(Review, review_id).to_dict()), 200
