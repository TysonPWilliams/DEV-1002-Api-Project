from flask import Blueprint, request
from init import db
from models.payment import Payment, many_payments, one_payment, payment_without_id

payments_bp = Blueprint('payments', __name__)

# Read all payments - GET /payments
@payments_bp.route('/payments')
def get_payments():
    stmt = db.Select(Payment)
    payments = db.session.scalars(stmt)
    return many_payments.dump(payments)

# Read one payment - GET /payments/<int:payment_id>
@payments_bp.route('/payments/<int:payment_id>')
def get_one_payment(payment_id):
    stmt = db.select(Payment).filter_by(id=payment_id)
    payment = db.session.scalar(stmt)
    if payment:
        return one_payment.dump(payment)
    else:
        return {"error": f"Payment with id {payment_id} not found! "}, 404
    
# Create a payment - POST /payments
@payments_bp.route('/payments', methods=['POST'])
def create_payment():
    ip_address = request.remote_addr  # Gets the user's IP address
    forwarded_for = request.headers.get('X-Forwarded-For')

    if forwarded_for:
        ip_address = forwarded_for.split(',')[0]  # Get the first IP in case of multiple proxies

    # Save IP address along with the payment details
    try:
        data = payment_without_id.load(request.json)

        new_payment = Payment(
            contract_id = data.get('contract_id'),
            amount = data.get('amount'),
            status = data.get('status'),
            payment_date = data.get('payment_date'),
            ip_address = ip_address,
            payment_method = data.get('payment_method')
        )

        db.session.add(new_payment)
        db.session.commit()
        return one_payment.dump(new_payment), 201
    
    except Exception as err:
        return {"Error": str(err)}, 400

# Update a payment - PUT and PATCH /payments/<int:payment_id>
@payments_bp.route('/payments/<int:payment_id>', methods=['PUT', 'PATCH'])
def update_payment(payment_id):
    try:
        stmt = db.select(Payment).filter_by(id=payment_id)
        payment = db.session.scalar(stmt)
        if payment:
            data = payment_without_id.load(request.json)

            payment.contract_id = data.get('contract_id') or payment.contract_id
            payment.amount = data.get('amount') or payment.amount
            payment.status = data.get('status') or payment.status
            payment.payment_date = data.get('payment_date') or payment.payment_date
            payment.ip_address = data.get('ip_address') or payment.ip_address
            payment.payment_method = data.get('payment_method') or payment.payment_method

            db.session.commit()
            return one_payment.dump(payment)
    
        else:
            return {"error": f"Payment with id {payment_id} not found! "}, 404
    
    except Exception as err:
        db.session.rollback()
        return {"Error": str(err)}

# Delete a payment - DELETE /payments/<int:payment_id>
@payments_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    try:
        stmt = db.select(Payment).filter_by(id=payment_id)
        payment = db.session.scalar(stmt)

        if payment:
            db.session.delete(payment)
            db.session.commit()

            return {}, 204
        
        else:
            return {"Error": f"Payment with id {payment_id} not found!"}, 404
        
    except Exception as err:
        return {"error", str(err)}