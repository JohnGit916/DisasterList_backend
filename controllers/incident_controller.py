from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.incident_report import IncidentReport

class IncidentListResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        location = data.get('location')

        if not title or not description or not location:
            return {'error': 'All fields are required'}, 400

        user_id = get_jwt_identity()

        incident = IncidentReport(
            title=title,
            description=description,
            location=location,
            user_id=user_id
        )
        db.session.add(incident)
        db.session.commit()

        return {
            'message': 'Incident reported successfully',
            'id': incident.id,
            'title': incident.title,
            'location': incident.location,
            'user_id': user_id
        }, 201

    def get(self):
        incidents = IncidentReport.query.all()
        result = []
        for i in incidents:
            result.append({
                "id": i.id,
                "title": i.title,
                "description": i.description,
                "location": i.location,
                "user_id": i.user_id
            })
        return result, 200


class IncidentResource(Resource):
    def get(self, id):
        incident = IncidentReport.query.get(id)
        if not incident:
            return {'error': 'Incident not found'}, 404
        return {
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "location": incident.location,
            "user_id": incident.user_id
        }, 200

    @jwt_required()
    def patch(self, id):
        user_id = get_jwt_identity()
        incident = IncidentReport.query.get(id)

        if not incident:
            return {'error': 'Incident not found'}, 404

        if str(incident.user_id) != str(user_id):
            return {'error': 'Unauthorized'}, 403

        data = request.get_json()
        incident.title = data.get('title', incident.title)
        incident.description = data.get('description', incident.description)
        incident.location = data.get('location', incident.location)

        db.session.commit()

        return {
            "message": "Incident updated successfully",
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "location": incident.location
        }, 200

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        incident = IncidentReport.query.get(id)

        if not incident:
            return {'error': 'Incident not found'}, 404

        if str(incident.user_id) != str(user_id):
            return {'error': 'Unauthorized'}, 403

        db.session.delete(incident)
        db.session.commit()
        return {'message': 'Incident deleted successfully'}, 200
