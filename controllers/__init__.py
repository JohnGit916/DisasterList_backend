from flask import Flask
from config import Config
from extensions import db
from models import User, IncidentReport, ResponseOffer


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Optionally register blueprints from controllers
    # from app.controllers.user_routes import user_bp
    # app.register_blueprint(user_bp)

    return app
