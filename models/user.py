from init import db, ma

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    address = db.Column(db.String(200))
    role = db.Column(db.String(20), nullable=False) # Need to validate with marshmallow validation, 3 options.

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'address', 'role')

one_user = UserSchema()
many_users = UserSchema(many=True)
user_without_id = UserSchema(exclude=['id'])