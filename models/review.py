from init import db, ma
from marshmallow_sqlalchemy import fields
from datetime import datetime, timezone

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id", ondelete='cascade'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    

class ReviewSchema(ma.Schema):
    contract_id = fields.Nested('ContractSchema')
    rating = fields.Int()

    class Meta:
        fields = ('id', 'job_id', 'freelancer_id', 'bid_amount', 'status', 'created_at')

one_review = ReviewSchema()
many_reviews = ReviewSchema(many=True)
review_without_id = ReviewSchema(exclude=['id'])