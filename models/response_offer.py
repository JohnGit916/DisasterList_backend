from extensions import db
from sqlalchemy.orm import relationship

class ResponseOffer(db.Model):
    __tablename__ = 'response_offers'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(20), default='pending')  # New field

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident_reports.id'), nullable=False)

    user = relationship("User", back_populates="offers")
    incident = relationship("IncidentReport", back_populates="offers")

    def __repr__(self):
        return f"<ResponseOffer from User {self.user_id} for Incident {self.incident_id}>"
