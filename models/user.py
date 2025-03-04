from init import db, ma

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    address = db.Column(db.String(200))
    role = db.Column(db.String(20), nullable=False) # Need to validate with marshmallow validation, 3 options.

    job = db.relationship('Job', back_populates='client')
    
    freelancer_contracts = db.relationship('Contract', foreign_keys='Contract.freelancer_id', back_populates='freelancer')
    client_contracts = db.relationship('Contract', foreign_keys='Contract.client_id', back_populates='client')

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'address', 'role')

one_user = UserSchema()
many_users = UserSchema(many=True)
user_without_id = UserSchema(exclude=['id'])