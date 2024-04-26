#!/usr/bin/python3
"""
This is a module that handls  Review objects
"""

from flask import jsonify, request, abort
from models import storage
from models.review import Review
from api.v1.views import app_views

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_for_place(place_id):
    """
    Method for Retrieving the list of all Review objects
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Method for Retrieving the list of all Review objects
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Method for Deleting a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Method for Creating a Review
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data or 'user_id' not in data or 'text' not in data:
        abort(400, 'Invalid JSON or missing required fields')
    user_id = data['user_id']
    if storage.get("User", user_id) is None:
        abort(404)
    new_review = Review(place_id=place_id, **data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Method for Updating a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Invalid JSON')
    for key in ('id', 'user_id', 'place_id', 'created_at', 'updated_at'):
        data.pop(key, None)
    for key, value in data.items():
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
