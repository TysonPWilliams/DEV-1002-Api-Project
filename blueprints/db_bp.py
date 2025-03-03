from flask import Blueprint
from init import db
from models.user import User

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('init')
def create_database():
    db.drop_all()
    db.create_all()
    print("Tables Created")

@db_bp.cli.command('seed')
def seed_database():
    users = [
        User(
            name = 'Tyson Williams',
            email = 'tysonwilliams@gmail.com',
            address = '30 Beckwith Street, Wagga Wagga',
            role = 'Admin'
        ),
        User(
            name = 'Jemimah Bailey',
            email = 'jemimahbailey@gmail.com',
            address = '30 Beckwith Street, Wagga Wagga',
            role = 'Freelancer'
        )
    ]

    db.session.add_all(users)
    db.session.commit()
    print("Database has been seeded")