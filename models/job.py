from init import db, ma
from marshmallow import fields, validate
from datetime import datetime, timezone
import pytz

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    budget = db.Column(db.DECIMAL(10, 2))
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))

    client = db.relationship('User', back_populates='job')
    contract = db.relationship('Contract', back_populates='job')
    application = db.relationship('Application', back_populates='job')


class JobSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True,
        validate=validate.Length(min=4, max=150, error="Title must be between 4 and 150 characters."))
    description = fields.Str()
    budget = fields.Decimal(as_string=True, places=2, validate=validate.Range(min=0))
    status = fields.Str(
        validate=validate.OneOf(["Open", "In Progress", "Completed", "Cancelled"], error="Invalid status, please enter either Open, In Progress, Completed or Cancelled")
    )
    client_id = fields.Int()
    client = fields.Nested(
        'UserSchema',
        exclude=[
            'address',
            'updated_at',
            'created_at'])
    created_at = fields.Function(
        lambda obj: obj.created_at.astimezone(pytz.timezone('Australia/Sydney')).strftime('%d/%m/%Y %H:%M %Z') if obj.created_at else None
    )   

    class Meta:
        fields = ('id', 'title', 'description', 'budget', 'status', 'client', 'client_id', 'created_at')

class JobListSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True,
        validate=validate.Length(min=4, max=150, error="Title must be between 4 and 150 characters."))
    description = fields.Str()
    budget = fields.Decimal(as_string=True, places=2, required=True, validate=validate.Range(min=0))
    status = fields.Str(
        required=True,
        validate=validate.OneOf(["Open", "In Progress", "Completed", "Cancelled"], error="Invalid status, please enter either Open, In Progress, Completed or Cancelled")
    )
    client_id = fields.Int()
    client = fields.Nested(
        'UserSchema',
        exclude=[
            'role',
            'created_at',
            'updated_at',
            'address'])
    created_at = fields.Function(
        lambda obj: obj.created_at.astimezone(pytz.timezone('Australia/Sydney')).strftime('%d/%m/%Y %H:%M %Z') if obj.created_at else None
    )   

    class Meta:
        fields = ('id', 'title', 'description', 'budget', 'status', 'client', 'created_at')

one_job = JobSchema()
many_jobs = JobListSchema(many=True)
job_without_id = JobSchema(exclude=['id'])