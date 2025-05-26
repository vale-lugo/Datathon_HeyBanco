from app import db
from sqlalchemy.orm import relationship

class ClientData(db.Model):
    __tablename__ = 'client_data'

    id = db.Column(db.String(40), primary_key=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    fecha_alta = db.Column(db.Date, nullable=True)
    id_municipio = db.Column(db.Integer, nullable=True)
    id_estado = db.Column(db.Integer, nullable=True)
    tipo_persona = db.Column(db.String(50), nullable=True)
    genero = db.Column(db.String(20), nullable=True)
    actividad_empresarial = db.Column(db.String(255), nullable=True)

    # Relationship with User
    users = relationship("User", back_populates="client")

    # Relationship with TransactionData
    transactions = relationship("TransactionData", back_populates="client")

    def __repr__(self):
        return f'<ClientData {self.id}>'
