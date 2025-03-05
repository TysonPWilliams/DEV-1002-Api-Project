from init import db, ma
from marshmallow_sqlalchemy import fields
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)

    contract_id = db.Column(db.Integer, db.ForeignKey("contracts.id", ondelete='cascade'))
    amount = db.Column(db.DECIMAL(10, 2))
    status = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime)

    

class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'contract_id', 'amount', 'status', 'payment_date')

one_payment = PaymentSchema()
many_payments = PaymentSchema(many=True)
payment_without_id = PaymentSchema(exclude=['id'])