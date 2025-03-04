from init import db, ma
from marshmallow_sqlalchemy import fields
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete='cascade'))
    freelancer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))
    bid_amount = db.Column(db.DECIMAL(10, 2))
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    

class ApplicationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'job_id', 'freelancer_id', 'bid_amount', 'status', 'created_at')

one_application = ApplicationSchema()
many_applications = ApplicationSchema(many=True)
application_without_id = ApplicationSchema(exclude=['id'])