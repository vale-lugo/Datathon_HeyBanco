import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get PostgreSQL URI from environment variables
postgres_uri = os.getenv("POSTGRES_URI")

# Create SQLAlchemy engine
engine = create_engine(postgres_uri)

# Create declarative base
Base = declarative_base()

# Define models
class Client(Base):
    __tablename__ = 'clients'

    # Auto-incrementing primary key
    client_pk = Column(Integer, primary_key=True, autoincrement=True)

    # Original ID from CSV (used for relationship)
    id = Column(String(255), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    fecha_alta = Column(Date, nullable=True)
    id_municipio = Column(Integer, nullable=True)
    id_estado = Column(Integer, nullable=True)
    tipo_persona = Column(String(255), nullable=True)
    genero = Column(String(1), nullable=True)
    actividad_empresarial = Column(Text, nullable=True)

    # Relationship with transactions
    transactions = relationship("Transaction", back_populates="client")

class Transaction(Base):
    __tablename__ = 'transactions'

    # Auto-incrementing primary key
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)

    # Client ID (foreign key)
    client_id = Column(String(255), ForeignKey('clients.id'), nullable=False)

    fecha = Column(Date, nullable=True)
    comercio = Column(String(255), nullable=True)
    giro_comercio = Column(Text, nullable=True)
    tipo_venta = Column(String(50), nullable=True)
    monto = Column(Float, nullable=True)

    # Relationship with client
    client = relationship("Client", back_populates="transactions")

def main():
    # Create tables
    Base.metadata.create_all(engine)

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Load clients data
        print("Loading clients data...")
        clients_df = pd.read_csv('data/raw/base_clientes_final.csv')

        # Convert date columns to datetime
        clients_df['fecha_nacimiento'] = pd.to_datetime(clients_df['fecha_nacimiento'], errors='coerce')
        clients_df['fecha_alta'] = pd.to_datetime(clients_df['fecha_alta'], errors='coerce')

        # Insert clients data
        for _, row in clients_df.iterrows():
            client = Client(
                id=row['id'],
                fecha_nacimiento=row['fecha_nacimiento'],
                fecha_alta=row['fecha_alta'],
                id_municipio=row['id_municipio'],
                id_estado=row['id_estado'],
                tipo_persona=row['tipo_persona'],
                genero=row['genero'],
                actividad_empresarial=row['actividad_empresarial']
            )
            session.add(client)

        # Commit clients data
        session.commit()
        print(f"Successfully loaded {len(clients_df)} client records")

        # Load transactions data
        print("Loading transactions data...")
        transactions_df = pd.read_csv('data/raw/base_transacciones_final.csv')

        # Convert date column to datetime
        transactions_df['fecha'] = pd.to_datetime(transactions_df['fecha'], errors='coerce')

        # Insert transactions data using pandas to_sql method
        # This avoids potential type conversion issues
        transactions_df.rename(columns={'id': 'client_id'}, inplace=True)

        # Use pandas to_sql with SQLAlchemy engine
        transactions_df.to_sql('transactions', engine, if_exists='append', index=False,
                              dtype={
                                  'client_id': String(255),
                                  'fecha': Date,
                                  'comercio': String(255),
                                  'giro_comercio': Text,
                                  'tipo_venta': String(50),
                                  'monto': Float
                              })

        print(f"Successfully loaded {len(transactions_df)} transaction records")

    except Exception as e:
        # Rollback in case of error
        session.rollback()
        print(f"Error: {e}")
    finally:
        # Close session
        session.close()

if __name__ == "__main__":
    main()
