from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.response_offer import ResponseOffer
from models.incident_report import IncidentReport
from models.user import User
from datetime import datetime

class OfferListResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        message = data.get('message')
        incident_id = data.get('incident_id')
        user_id = get_jwt_identity()

        if not message or not incident_id:
            return {'error': 'Message and incident_id are required'}, 400

        incident = IncidentReport.query.get(incident_id)
        if not incident:
            return {'error': 'Incident not found'}, 404

        new_offer = ResponseOffer(
            message=message,
            incident_id=incident_id,
            user_id=user_id,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_offer)
        db.session.commit()

        user = User.query.get(user_id)

        return {
            "message": "Offer submitted successfully",
            "id": new_offer.id,
            "incident_id": incident_id,
            "user_id": user_id,
            "username": user.username if user else None,
            "status": new_offer.status,
            "timestamp": new_offer.timestamp.isoformat()
        }, 201

    def get(self):
        incident_id = request.args.get('incident_id')
        query = ResponseOffer.query
        if incident_id:
            query = query.filter_by(incident_id=incident_id)

        offers = query.all()
        result = []
        for o in offers:
            user = User.query.get(o.user_id)
            result.append({
                "id": o.id,
                "message": o.message,
                "incident_id": o.incident_id,
                "user_id": o.user_id,
                "username": user.username if user else None,
                "status": o.status,
                "timestamp": o.timestamp.isoformat()
            })
        return result, 200


class OfferResource(Resource):
    @jwt_required()
    def put(self, id):
        user_id = int(get_jwt_identity())
        offer = ResponseOffer.query.get(id)

        if not offer:
            return {'error': 'Offer not found'}, 404

        incident = IncidentReport.query.get(offer.incident_id)
        if not incident:
            return {'error': 'Incident not found'}, 404

        data = request.get_json()

        updated = False

        if offer.user_id == user_id and 'message' in data:
            offer.message = data['message']
            updated = True

        if incident.user_id == user_id and 'status' in data:
            new_status = data['status']
            if new_status not in ['pending', 'accepted', 'rejected']:
                return {"error": "Invalid status value"}, 400
            offer.status = new_status
            updated = True

        if not updated:
            return {'error': 'Unauthorized to update this offer'}, 403

        db.session.commit()

        return {
            "message": "Offer updated successfully",
            "id": offer.id,
            "message_text": offer.message,
            "status": offer.status
        }, 200

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        offer = ResponseOffer.query.get(id)

        if not offer:
            return {'error': 'Offer not found'}, 404
        if str(offer.user_id) != str(user_id):
            return {'error': 'Unauthorized'}, 403

        db.session.delete(offer)
        db.session.commit()
        return {'message': 'Offer deleted successfully'}, 200
