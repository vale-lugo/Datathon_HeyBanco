from app import db
from sqlalchemy.orm import relationship

class TransactionData(db.Model):
    __tablename__ = 'transaction_data'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=True)
    comercio = db.Column(db.String(100), nullable=True)
    giro_comercio = db.Column(db.String(100), nullable=True)
    tipo_venta = db.Column(db.String(50), nullable=True)
    monto = db.Column(db.Float, nullable=True)
    client_id = db.Column(db.String(40), db.ForeignKey('client_data.id'), nullable=True)

    # Relationship with ClientData
    client = relationship("ClientData", back_populates="transactions")

    def __repr__(self):
        return f'<TransactionData {self.id}>'
