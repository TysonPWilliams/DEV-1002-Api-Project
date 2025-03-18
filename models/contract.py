from init import db, ma
from marshmallow import fields, validate, validates_schema, ValidationError
from datetime import datetime, date

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete='cascade'))
    freelancer_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))
    client_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), nullable=False)

    freelancer = db.relationship('User', foreign_keys=[freelancer_id], back_populates='freelancer_contracts')
    client = db.relationship('User', foreign_keys=[client_id], back_populates='client_contracts')
    job = db.relationship('Job', back_populates='contract')

    

class ContractSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    job_id = fields.Int(required=True)
    freelancer_id = fields.Int(required=True)
    client_id = fields.Int(required=True)
    start_date = fields.Date(
        required=True,
        validate=validate.Range(
            min=date.today(), error="Start date must be today or in the future."
        )
    )
    end_date = fields.Date(required=True)
    status = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["Pending", "Active", "Completed", "Cancelled"],
            error="Invalid status, must be Pending, Active, Completed, or Cancelled."
        )
    )
    freelancer = fields.Nested('UserSchema', exclude=['id', 'role', 'address', 'created_at', 'updated_at'])
    client = fields.Nested('UserSchema', exclude=['id', 'role', 'address', 'updated_at', 'created_at'])
    job = fields.Nested('JobSchema', exclude=['id', 'client', 'created_at'])

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if "start_date" in data and "end_date" in data:
            if data["end_date"] < data["start_date"]:
                raise ValidationError("End date must be after start date.", field_name="end_date")

    class Meta:
        model = Contract
        load_instance = True
        fields = ('id', 'job', 'job_id', 'freelancer', 'freelancer_id', 'client', 'client_id', 'start_date', 'end_date', 'status')

class ContractListSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    client_id = fields.Int()
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Str()

    job = fields.Nested('JobSchema', exclude=['description', 'budget', 'client', 'status', 'created_at', 'client_id'])
    freelancer = fields.Nested('UserSchema', exclude=['email', 'address', 'role', 'is_active', 'created_at', 'updated_at'])
    client = fields.Nested('UserSchema', exclude=['email', 'address', 'role', 'is_active', 'created_at', 'updated_at'])
    
    class Meta:
        model = Contract
        load_instance = True
        fields = ('id', 'job', 'freelancer', 'client', 'start_date', 'end_date', 'status')
    

    

one_contract = ContractSchema()
many_contracts = ContractListSchema(many=True)
contract_without_id = ContractSchema(only=['job_id', 'freelancer_id', 'client_id', 'start_date', 'end_date', 'status'])