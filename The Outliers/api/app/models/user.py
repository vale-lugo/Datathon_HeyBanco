from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.String(40), db.ForeignKey('client_data.id'), nullable=True)

    # Relationship with ClientData
    client = relationship("ClientData", back_populates="users")

    def __repr__(self):
        return f'<User {self.username}>'
