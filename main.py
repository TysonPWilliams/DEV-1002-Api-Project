from flask import Flask
from dotenv import load_dotenv
import os
from init import db, ma
from blueprints.db_bp import db_bp
from blueprints.users_bp import users_bp
from blueprints.jobs_bp import jobs_bp
from blueprints.applications_bp import applications_bp
from blueprints.contracts_bp import contracts_bp
from blueprints.reviews_bp import reviews_bp

def create_app():
    app = Flask(__name__)

    load_dotenv(override=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(contracts_bp)
    app.register_blueprint(reviews_bp)


    return app