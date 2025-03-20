from flask import Blueprint, request
from init import db
from models.contract import Contract, many_contracts, one_contract, contract_without_id
from datetime import datetime, timezone

contracts_bp = Blueprint('contracts', __name__)

# Read all contracts - GET /contracts
@contracts_bp.route('/contracts')
def get_contracts():
    stmt = db.Select(Contract)
    contracts = db.session.scalars(stmt)
    return many_contracts.dump(contracts)

# Read one contract - GET /contracts/<int:contract_id>
@contracts_bp.route('/contracts/<int:contract_id>')
def get_one_contract(contract_id):
    stmt = db.select(Contract).filter_by(id=contract_id)
    contract = db.session.scalar(stmt)
    if contract:
        return one_contract.dump(contract)
    else:
        return {"error": f"Contract with id {contract_id} not found! "}, 404
    
# Create a contract - POST /contracts
@contracts_bp.route('/contracts', methods=['POST'])
def create_contract():
    try:
        data = contract_without_id.load(request.json)

        new_contract = Contract(
            job_id = data.get('job_id'),
            freelancer_id = data.get('freelancer_id'),
            client_id = data.get('client_id'),
            start_date = data.get('start_date'),
            end_date = data.get('end_date'),
            created_at = datetime.now(timezone.utc)
        )

        db.session.add(new_contract)
        db.session.commit()
        return one_contract.dump(new_contract), 201
    
    except Exception as err:
        return {"Error": str(err)}, 400

# Update a contract - PUT and PATCH /contracts/<int:contract_id>
@contracts_bp.route('/contracts/<int:contract_id>', methods=['PUT', 'PATCH'])
def update_contract(contract_id):
    try:
        stmt = db.select(Contract).filter_by(id=contract_id)
        contract = db.session.scalar(stmt)
        if contract:
            data = contract_without_id.load(request.json)

            contract.job_id = data.get('job_id') or contract.job_id
            contract.freelancer_id = data.get('freelancer_id') or contract.freelancer_id
            contract.client_id = data.get('client_id') or contract.client_id
            contract.start_date = data.get('start_date') or contract.start_date
            contract.end_date = data.get('end_date') or contract.end_date
            contract.created_at = data.get('created_at') or contract.created_at

            db.session.commit()
            return one_contract.dump(contract)
    
        else:
            return {"error": f"Contract with id {contract_id} not found! "}, 404
    
    except Exception as err:
        db.session.rollback()
        return {"Error": str(err)}

# Delete a contract - DELETE /contracts/<int:contract_id>
@contracts_bp.route('/contracts/<int:contract_id>', methods=['DELETE'])
def delete_contract(contract_id):
    try:
        stmt = db.select(Contract).filter_by(id=contract_id)
        contract = db.session.scalar(stmt)

        if contract:
            db.session.delete(contract)
            db.session.commit()

            return {}, 204
        
        else:
            return {"Error": f"Contract with id {contract_id} not found!"}, 404
        
    except Exception as err:
        return {"error", str(err)}