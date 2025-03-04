from init import db, ma

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    budget = db.Column(db.Decimal(10, 2))
    status = db.Column(db.String(20), nullable=False)
    client_id = db.Column(db.Integer, ForeignKey=True)

class JobSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'address', 'role')

one_job = JobSchema()
many_jobs = JobSchema(many=True)
job_without_id = JobSchema(exclude=['id'])