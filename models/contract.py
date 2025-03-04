from init import db, ma
from marshmallow import fields
from datetime import datetime, date

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete='cascade'))
    freelancer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))
    client_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.Date, default=datetime.utcnow)

    freelancer = db.relationship('User', foreign_keys=[freelancer_id], back_populates='freelancer_contracts')
    client = db.relationship('User', foreign_keys=[client_id], back_populates='client_contracts')

    

class ContractSchema(ma.Schema):
    created_at = fields.DateTime(format="%Y-%m-%d")
    freelancer_id = fields.Nested('UserSchema', exclude=['role', 'address'])
    client_id = fields.Nested('UserSchema', exclude=['role', 'address'])

    class Meta:
        fields = ('id', 'job_id', 'freelancer_id', 'freelancer' 'client_id', 'start_date', 'end_date', 'created_at')

one_contract = ContractSchema()
many_contracts = ContractSchema(many=True)
contract_without_id = ContractSchema(exclude=['id'])