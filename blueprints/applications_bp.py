from flask import Blueprint, request
from init import db
from models.application import Application, many_applications, one_application, application_without_id
from datetime import datetime, timezone

applications_bp = Blueprint('applications', __name__)

# Read all applications - GET /applications
@applications_bp.route('/applications')
def get_applications():
    stmt = db.Select(Application)
    applications = db.session.scalars(stmt)
    return many_applications.dump(applications)

# Read one application - GET /applications/<int:application_id>
@applications_bp.route('/applications/<int:application_id>')
def get_one_application(application_id):
    stmt = db.select(Application).filter_by(id=application_id)
    application = db.session.scalar(stmt)
    if application:
        return one_application.dump(application)
    else:
        return {"error": f"Application with id {application_id} not found! "}, 404
    
# Create a application - POST /applications
@applications_bp.route('/applications', methods=['POST'])
def create_application():
    try:
        data = application_without_id.load(request.json)

        new_application = Application(
            job_id = data.get('job_id'),
            freelancer_id = data.get('freelancer_id'),
            bid_amount = data.get('bid_amount'),
            status = data.get('status'),
            created_at = datetime.now(timezone.utc)
        )

        db.session.add(new_application)
        db.session.commit()
        return one_application.dump(new_application), 201
    
    except Exception as err:
        return {"Error": str(err)}, 400

# Update a application - PUT and PATCH /applications/<int:application_id>
@applications_bp.route('/applications/<int:application_id>', methods=['PUT', 'PATCH'])
def update_application(application_id):
    try:
        stmt = db.select(Application).filter_by(id=application_id)
        application = db.session.scalar(stmt)
        if application:
            data = application_without_id.load(request.json)

            application.job_id = data.get('job_id') or application.job_id
            application.freelancer_id = data.get('freelancer_id') or application.freelancer_id
            application.bid_amount = data.get('bid_amount') or application.bid_amount
            application.status = data.get('status') or application.status
            application.created_at = data.get('created_at') or application.created_at

            db.session.commit()
            return one_application.dump(application)
    
        else:
            return {"error": f"Application with id {application_id} not found! "}, 404
    
    except Exception as err:
        db.session.rollback()
        return {"Error": str(err)}

# Delete a application - DELETE /applications/<int:application_id>
@applications_bp.route('/applications/<int:application_id>', methods=['DELETE'])
def delete_application(application_id):
    try:
        stmt = db.select(Application).filter_by(id=application_id)
        application = db.session.scalar(stmt)

        if application:
            db.session.delete(application)
            db.session.commit()

            return {}, 204
        
        else:
            return {"Error": f"Application with id {application_id} not found!"}, 404
        
    except Exception as err:
        return {"error", str(err)}