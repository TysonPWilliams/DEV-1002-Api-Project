from init import db, ma
from marshmallow import fields, validate

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    address = db.Column(db.String(200))
    role = db.Column(db.String(20), nullable=False) # Need to validate with marshmallow validation, 3 options.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    job = db.relationship('Job', back_populates='client')
    
    freelancer_contracts = db.relationship('Contract', foreign_keys='Contract.freelancer_id', back_populates='freelancer')
    client_contracts = db.relationship('Contract', foreign_keys='Contract.client_id', back_populates='client')

class UserSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True, unique=True)
    address = fields.Str()
    role = fields.Str(
        required=True,
        validate=validate.OneOf(["Freelancer", "Admin", "Client"], error="Invalid role, must be Freelancer, Admin, or Client.")
    )
    # is_active = fields.Boolean(dump_only=False)
    # created_at = fields.DateTime(dump_only=True)
    # updated_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = ('id', 'name', 'email', 'address', 'role')

one_user = UserSchema()
many_users = UserSchema(many=True)
user_without_id = UserSchema(exclude=['id'])