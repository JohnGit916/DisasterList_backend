from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    reports = relationship("IncidentReport", back_populates="user", cascade="all, delete")
    offers = relationship("ResponseOffer", back_populates="user", cascade="all, delete")

    # Many-to-many (via ResponderIncident)
    responded_incidents = relationship("ResponderIncident", back_populates="responder", cascade="all, delete")

    def __repr__(self):
        return f"<User {self.username}>"
