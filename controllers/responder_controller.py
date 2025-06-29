from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.responder_incident import ResponderIncident
from models.incident_report import IncidentReport

class ResponderIncidentResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        role = data.get('role')
        note = data.get('note', "")
        incident_id = data.get('incident_id')
        user_id = int(get_jwt_identity())

        if not role or not incident_id:
            return {'error': 'Role and incident_id required'}, 400

        incident = IncidentReport.query.get(incident_id)
        if not incident:
            return {'error': 'Incident not found'}, 404

        existing = ResponderIncident.query.filter_by(user_id=user_id, incident_id=incident_id).first()
        if existing:
            return {'error': 'Already enlisted for this incident'}, 409

        responder = ResponderIncident(
            user_id=user_id,
            incident_id=incident_id,
            role=role,
            note=note
        )
        db.session.add(responder)
        db.session.commit()

        return {
            'message': 'You have been added to this incident',
            'incident_id': incident_id,
            'role': role,
            'status': responder.status,
            'timestamp': responder.timestamp.isoformat() if responder.timestamp else None
        }, 201

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        incident_id = request.args.get("incident_id")

        query = ResponderIncident.query.filter_by(user_id=user_id)

        if incident_id:
            query = query.filter_by(incident_id=incident_id)

        responses = query.all()

        return [{
            'incident_id': r.incident_id,
            'role': r.role,
            'note': r.note,
            'status': r.status,
            'timestamp': r.timestamp.isoformat() if r.timestamp else None
        } for r in responses], 200
