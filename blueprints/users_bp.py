from flask import Blueprint
from init import db
from models.user import User, many_users, one_user, user_without_id

users_bp = Blueprint('users', __name__)

# Read all users - GET /users
@users_bp.route('/users')
def get_users():
    stmt = db.Select(User).order_by(User.name)
    students = db.session.scalars(stmt)
    return many_users.dump(students)

# Read one user - GET /users/<int:user_id>
@users_bp.route('/users/<int:user_id')
def get_one_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalars(stmt)
    if user:
        return one_user.dump(user)
    else:
        return {"error": f"User with id {user_id} not found! "}, 404
    
# Create a user - POST /users
# Update a user - PUT and PATCH /users/<int:user_id>
# Delete a user - DELETE /users/<int:user_id>