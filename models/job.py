from init import db, ma
from marshmallow_sqlalchemy import fields
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    budget = db.Column(db.DECIMAL(10, 2))
    status = db.Column(db.String(20), nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))

    client = db.relationship('User', back_populates='job')
    contract = db.relationship('Contract', back_populates='job')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobSchema(ma.Schema):

    client = fields.Nested('UserSchema', exclude=['id', 'address', 'role'])

    class Meta:
        fields = ('id', 'title', 'description', 'budget', 'status', 'client_id', 'client', 'created_at')

one_job = JobSchema()
many_jobs = JobSchema(many=True)
job_without_id = JobSchema(exclude=['id'])