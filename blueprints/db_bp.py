from flask import Blueprint
from init import db
from models.user import User
from models.job import Job

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

    jobs = [
        Job(
            title = "Simple Website Creation",
            description = "Needed a web developer to create a deploy a simple website",
            budget = 500,
            status = "Not yet assigned",
            client_id = 1
        )
    ]
    print("Database has been seeded")