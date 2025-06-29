from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.response_offer import ResponseOffer
from models.incident_report import IncidentReport

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
            user_id=user_id
        )
        db.session.add(new_offer)
        db.session.commit()

        return {
            "message": "Offer submitted successfully",
            "id": new_offer.id,
            "incident_id": incident_id,
            "user_id": user_id,
            "status": new_offer.status,
            "timestamp": new_offer.timestamp.isoformat()
        }, 201

    def get(self):
        incident_id = request.args.get('incident_id')
        query = ResponseOffer.query
        if incident_id:
            query = query.filter_by(incident_id=incident_id)

        offers = query.all()
        return [{
            "id": o.id,
            "message": o.message,
            "incident_id": o.incident_id,
            "user_id": o.user_id,
            "status": o.status,
            "timestamp": o.timestamp.isoformat()
        } for o in offers], 200


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

        # Allow the offer creator to update their own message
        if offer.user_id == user_id:
            offer.message = data.get('message', offer.message)

        # Allow the incident owner to update offer status
        if incident.user_id == user_id:
            new_status = data.get('status')
            if new_status:
                if new_status not in ['pending', 'accepted', 'rejected']:
                    return {"error": "Invalid status value"}, 400
                offer.status = new_status

        # If neither condition applies, unauthorized
        if offer.user_id != user_id and incident.user_id != user_id:
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
