from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from extensions import db, migrate, jwt
from config import Config

# Import resources
from controllers.auth_controller import SignupResource, LoginResource, LogoutResource
from controllers.incident_controller import IncidentListResource, IncidentResource
from controllers.offer_controller import OfferListResource, OfferResource
from controllers.responder_controller import ResponderIncidentResource  # ✅ Add this line

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api = Api(app)

    # Auth routes
    api.add_resource(SignupResource, '/signup')
    api.add_resource(LoginResource, '/login')
    api.add_resource(LogoutResource, '/logout')

    # Incident routes
    api.add_resource(IncidentListResource, '/incidents')
    api.add_resource(IncidentResource, '/incidents/<int:id>')

    # Offer routes
    api.add_resource(OfferListResource, '/offers')
    api.add_resource(OfferResource, '/offers/<int:id>')

    # Responder routes (for many-to-many responder_incident table)
    api.add_resource(ResponderIncidentResource, '/responders')  # ✅ Active route

    @app.route('/')
    def home():
        return {'message': 'DisasterLink API is running'}

    return app

# Flask CLI support
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
