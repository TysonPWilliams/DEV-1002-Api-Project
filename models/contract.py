from init import db, ma
from marshmallow import fields
from datetime import datetime, timezone
import pytz

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete='cascade'))
    freelancer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))
    client_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    status = db.Column(db.String(50))

    freelancer = db.relationship('User', foreign_keys=[freelancer_id], back_populates='freelancer_contracts')
    client = db.relationship('User', foreign_keys=[client_id], back_populates='client_contracts')
    job = db.relationship('Job', back_populates='contract')
    review = db.relationship('Review', back_populates='contract')
    

class ContractSchema(ma.Schema):
    
    created_at = fields.DateTime(format="%Y-%m-%d")
    client_id = fields.Int()

    created_at = fields.Function(
        lambda obj: obj.created_at.astimezone(pytz.timezone('Australia/Sydney')).strftime('%d/%m/%Y %H:%M %Z') if obj.created_at else None
    )   
    freelancer = fields.Nested(
        'UserSchema',
        exclude=[
            'role',
            'address',
            'created_at',
            'updated_at',
            'email'])
    
    client = fields.Nested(
        'UserSchema',
        exclude=[
            'role',
            'address',
            'created_at',
            'updated_at',
            'email'])
    
    job = fields.Nested('JobSchema', exclude=['client_id', 'client', 'created_at', 'budget'])
    
    class Meta:
        fields = ('id', 'job', 'freelancer', 'freelancer_id', 'client_id', 'job_id', 'client', 'created_at', 'start_date', 'end_date', 'status')
    

    

one_contract = ContractSchema()
many_contracts = ContractSchema(many=True)
contract_without_id = ContractSchema(exclude=['id'])