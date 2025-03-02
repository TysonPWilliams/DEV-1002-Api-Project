from flask import Blueprint
from init import db

db_bp = Blueprint('db', __name__)

@db_bp.cli.command('init')
def create_database():
    db.drop_all()
    db.create_all()
    print("Tables Created")