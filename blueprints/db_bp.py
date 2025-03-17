from flask import Blueprint
from init import db
from datetime import datetime
from models.user import User
from models.job import Job
from models.application import Application
from models.contract import Contract

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
            role = 'Admin',
            is_active = True
        ),
        User(
            name = 'Jemimah Bailey',
            email = 'jemimahbailey@gmail.com',
            address = '30 Beckwith Street, Wagga Wagga',
            role = 'Freelancer',
            is_active = True
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

    db.session.add_all(jobs)
    db.session.commit()

    applications = [
        Application(
            job_id = 1,
            freelancer_id = 1,
            bid_amount = 450,
            status = "In progress"
        )
    ]

    db.session.add_all(applications)
    db.session.commit()
    
    contracts = [
        Contract(
            job_id = 1,
            freelancer_id = 1,
            client_id = 2,
            start_date = "2025-03-04",
            end_date = "2025-04-04",
            status = "Not yet accepted"
        )
    ]

    db.session.add_all(contracts)
    db.session.commit()

    print("Database has been seeded")