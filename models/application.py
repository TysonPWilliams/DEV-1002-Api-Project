from init import db, ma
from marshmallow import fields, validate
from datetime import datetime, timezone
import pytz

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete='cascade'))
    freelancer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))
    bid_amount = db.Column(db.DECIMAL(10, 2))
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    freelancer = db.relationship('User', foreign_keys=[freelancer_id], back_populates='freelancer_application')
    job = db.relationship('Job', back_populates='application')

class ApplicationSchema(ma.Schema):
    id = fields.Int()
    job_id = fields.Int()
    freelancer_id = fields.Int()
    bid_amount = fields.Decimal(as_string=True, places=2, validate=validate.Range(min=0))
    created_at = fields.Function(
        lambda obj: obj.created_at.astimezone(pytz.timezone('Australia/Sydney')).strftime('%d/%m/%Y %H:%M %Z') if obj.created_at else None
    ) 

    status = fields.Str(
        validate=validate.OneOf(["Pending", "Approved", "Rejected", "Withdrawn", "Expired"], error="Error, please enter either Pending, Approved, Rejected, Withdrawn or Expired"))
    
    freelancer = fields.Nested(
        'UserSchema',
        exclude=(
        'address',
        'created_at',
        'email',
        'updated_at',
        'role',
        'is_active',
        'id'
        ))

    job = fields.Nested(
        'JobSchema',
        exclude=(
            'budget',
            'description',
            'client.email',
            'client.role',
            'created_at',
            'id',
            'client.is_active',
            'client_id'
        ))

    class Meta:
        fields = ('id', 'job_id', 'freelancer_id', 'job', 'freelancer', 'bid_amount', 'status', 'created_at')

one_application = ApplicationSchema()
many_applications = ApplicationSchema(many=True)
application_without_id = ApplicationSchema(exclude=['id'])