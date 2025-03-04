from flask import Flask
from dotenv import load_dotenv
import os
from init import db, ma
from blueprints.db_bp import db_bp
from blueprints.users_bp import users_bp
from blueprints.jobs_bp import jobs_bp
from blueprints.applications_bp import applications_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)

    return app