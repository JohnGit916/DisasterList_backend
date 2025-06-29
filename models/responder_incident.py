# models/responder_incident.py
from extensions import db
from sqlalchemy.orm import relationship

class ResponderIncident(db.Model):
    __tablename__ = 'responder_incidents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident_reports.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text)

    # ✅ Make sure these exist!
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(50), default='active')

    responder = relationship("User", back_populates="responded_incidents")
    incident = relationship("IncidentReport", back_populates="responder_entries")


    def __repr__(self):
        return f"<ResponderIncident User={self.user_id} Incident={self.incident_id} Role={self.role}>"
