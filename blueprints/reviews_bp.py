from flask import Blueprint, request
from init import db
from models.review import Review, many_reviews, one_review, review_without_id
from datetime import datetime, timezone

reviews_bp = Blueprint('reviews', __name__)

# Read all reviews - GET /reviews
@reviews_bp.route('/reviews')
def get_reviews():
    stmt = db.Select(Review)
    reviews = db.session.scalars(stmt)
    return many_reviews.dump(reviews)

# Read one review - GET /reviews/<int:review_id>
@reviews_bp.route('/reviews/<int:review_id>')
def get_one_review(review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        return one_review.dump(review)
    else:
        return {"error": f"Review with id {review_id} not found! "}, 404
    
# Create a review - POST /reviews
@reviews_bp.route('/reviews', methods=['POST'])
def create_review():
    try:
        
        data = review_without_id.load(request.json)

        new_review = Review(
            contract_id = data.get('contract_id'),
            rating = data.get('rating'),
            comment = data.get('comment'),
            created_at = datetime.now(timezone.utc)
        )

        db.session.add(new_review)
        db.session.commit()
        return one_review.dump(new_review), 201
    
    except Exception as err:
        return {"Error": str(err)}, 400

# Update a review - PUT and PATCH /reviews/<int:review_id>
@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT', 'PATCH'])
def update_review(review_id):
    try:
        stmt = db.select(Review).filter_by(id=review_id)
        review = db.session.scalar(stmt)
        if review:
            data = review_without_id.load(request.json)

            review.contract_id = data.get('contract_id') or review.contract_id
            review.rating = data.get('rating') or review.rating
            review.comment = data.get('comment') or review.comment
            review.created_at = data.get('created_at') or review.created_at

            db.session.commit()
            return one_review.dump(review)
    
        else:
            return {"error": f"Review with id {review_id} not found! "}, 404
    
    except Exception as err:
        db.session.rollback()
        return {"Error": str(err)}

# Delete a review - DELETE /reviews/<int:review_id>
@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        stmt = db.select(Review).filter_by(id=review_id)
        review = db.session.scalar(stmt)

        if review:
            db.session.delete(review)
            db.session.commit()

            return {}, 204
        
        else:
            return {"Error": f"Review with id {review_id} not found!"}, 404
        
    except Exception as err:
        return {"error", str(err)}