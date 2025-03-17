from flask import Blueprint, request
from init import db
from models.job import Job, many_jobs, one_job, job_without_id
from datetime import datetime, timezone

jobs_bp = Blueprint('jobs', __name__)

# Read all jobs - GET /jobs
@jobs_bp.route('/jobs')
def get_jobs():
    stmt = db.Select(Job).order_by(Job.title)
    jobs = db.session.scalars(stmt)
    return many_jobs.dump(jobs)

# Read one job - GET /jobs/<int:job_id>
@jobs_bp.route('/jobs/<int:job_id>')
def get_one_job(job_id):
    stmt = db.select(Job).filter_by(id=job_id)
    job = db.session.scalar(stmt)
    if job:
        return one_job.dump(job)
    else:
        return {"error": f"Job with id {job_id} not found! "}, 404
    
# Create a job - POST /jobs
@jobs_bp.route('/jobs', methods=['POST'])
def create_job():
    try:
        data = job_without_id.load(request.json)

        new_job = Job(
            title = data.get('title'),
            description = data.get('description'),
            budget = data.get('budget'),
            status = data.get('status'),
            client_id = data.get('client_id'),
            created_at = datetime.now(timezone.utc)
        )

        db.session.add(new_job)
        db.session.commit()
        return one_job.dump(new_job), 201
    
    except Exception as err:
        return {"Error": str(err)}, 400

# Update a job - PUT and PATCH /jobs/<int:job_id>
@jobs_bp.route('/jobs/<int:job_id>', methods=['PUT', 'PATCH'])
def update_job(job_id):
    try:
        stmt = db.select(Job).filter_by(id=job_id)
        job = db.session.scalar(stmt)
        if job:
            data = job_without_id.load(request.json)

            job.title = data.get('title') or job.title
            job.description = data.get('description') or job.description
            job.budget = data.get('budget') or job.budget
            job.status = data.get('status') or job.status
            job.client_id = data.get('client_id') or job.client_id
            job.created_at = data.get('created_at') or job.created_at

            db.session.commit()
            return one_job.dump(job)
    
        else:
            return {"error": f"Job with id {job_id} not found! "}, 404
    
    except Exception as err:
        db.session.rollback()
        return {"Error": str(err)}

# Delete a job - DELETE /jobs/<int:job_id>
@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        stmt = db.select(Job).filter_by(id=job_id)
        job = db.session.scalar(stmt)

        if job:
            db.session.delete(job)
            db.session.commit()

            return {}, 204
        
        else:
            return {"Error": f"Job with id {job_id} not found!"}, 404
        
    except Exception as err:
        return {"error", str(err)}