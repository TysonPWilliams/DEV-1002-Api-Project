from flask import Blueprint, request
from init import db
from models.user import User, many_users, one_user, user_without_id
from datetime import datetime, timezone
from marshmallow import ValidationError

users_bp = Blueprint('users', __name__)

# Read all users - GET /users
@users_bp.route('/users')
def get_users():
    stmt = db.Select(User).order_by(User.name)
    users = db.session.scalars(stmt)
    return many_users.dump(users)

# Read one user - GET /users/<int:user_id>
@users_bp.route('/users/<int:user_id>')
def get_one_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        return one_user.dump(user)
    else:
        return {"error": f"User with id {user_id} not found! "}, 404
    
# Create a user - POST /users
@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = user_without_id.load(request.json)

        new_user = User(
            name = data.get('name'),
            email = data.get('email'),
            address = data.get('address'),
            role = data.get('role'),
            is_active = data.get('is_active', True),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)  
        )

        print("New User Object:", new_user)  # Debugging

        db.session.add(new_user)
        db.session.commit()
        return one_user.dump(new_user), 201
    
    except ValidationError as err:
        return {"Error": str(err)}, 400
    except Exception as err:
        return {"Error": str(err)}, 400

# Update a user - PUT and PATCH /users/<int:user_id>
@users_bp.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    try:
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user:
            data = user_without_id.load(request.json)

            user.name = data.get('name') or user.name
            user.email = data.get('email') or user.email
            user.address = data.get('address') or user.address
            user.role = data.get('role') or user.role
            user.is_active = data.get('is_active') or user.is_active
            user.created_at = data.get('created_at') or user.created_at
            user.updated_at = datetime.now(timezone.utc)
            
            db.session.commit()
            return one_user.dump(user)
    
        else:
            return {"error": f"User with id {user_id} not found! "}, 404
    
    except Exception as err:
        db.session.rollback()
        return {"Error": str(err)}

# Delete a user - DELETE /users/<int:user_id>
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        if user:
            db.session.delete(user)
            db.session.commit()

            return {}, 204
        
        else:
            return {"Error": f"User with id {user_id} not found!"}, 404
        
    except Exception as err:
        return {"error", str(err)}