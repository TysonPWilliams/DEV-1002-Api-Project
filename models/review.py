from init import db, ma
from marshmallow import fields, validate
from datetime import datetime, timezone
import pytz

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id", ondelete='cascade'))
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    contract = db.relationship('Contract', back_populates='review')
    

class ReviewSchema(ma.Schema):
    contract_id = fields.Int()
    contract = fields.Nested('ContractSchema', exclude=[
        'client.created_at',
        'client.updated_at',
        'freelancer.created_at',
        'freelancer.updated_at',
        'job.budget',
        'status'])
    rating = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=10, error="Rating must be between 0 and 10.")
    )
    comment = fields.Str(
        validate=validate.Length(min=4, max=500, error="Comment must be between 4 and 500 characters.")
    )
    created_at = fields.Function(
        lambda obj: obj.created_at.astimezone(pytz.timezone('Australia/Sydney')).strftime('%d/%m/%Y %H:%M %Z') if obj.created_at else None
    )

    class Meta:
        fields = ('id', 'contract_id', 'contract', 'rating', 'comment', 'created_at')

class ReviewListSchema(ma.Schema):
    contract_id = fields.Int(required=True)
    contract = fields.Nested(
        'ContractSchema',
        exclude=['id',
                'job',
                'start_date',
                'end_date',
                'client.created_at',
                'client.email',
                'client.is_active',
                'client.updated_at',
                'freelancer.created_at',
                'freelancer.email',
                'freelancer.is_active',
                'freelancer.updated_at',])
    rating = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=10, error="Rating must be between 0 and 10.")
    )
    comment = fields.Str(
        validate=validate.Length(min=4, max=500, error="Comment must be between 4 and 500 characters.")
    )
    created_at = fields.Function(
        lambda obj: obj.created_at.astimezone(pytz.timezone('Australia/Sydney')).strftime('%d/%m/%Y %H:%M %Z') if obj.created_at else None
    )

    class Meta:
        fields = ('id', 'contract_id', 'contract', 'rating', 'comment', 'created_at')

one_review = ReviewSchema()
many_reviews = ReviewListSchema(many=True)
review_without_id = ReviewSchema(exclude=['id'])