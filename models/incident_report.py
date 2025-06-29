from extensions import db
from sqlalchemy.orm import relationship

class IncidentReport(db.Model):
    __tablename__ = 'incident_reports'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="reports")

    offers = relationship("ResponseOffer", back_populates="incident", cascade="all, delete")
    responder_entries = relationship("ResponderIncident", back_populates="incident", cascade="all, delete")

    def __repr__(self):
        return f"<IncidentReport {self.title}>"
