from app import create_app, db
from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy import inspect
from app.models.client_data import ClientData

# Load environment variables from .env file
load_dotenv()

def main():
    app = create_app()

    with app.app_context():
        try:
            # Print the model definition
            print("\nClientData model definition:")
            for column in ClientData.__table__.columns:
                print(f"Column: {column.name}, Type: {column.type}")

            # Drop all tables
            print("\nDropping all tables...")
            db.drop_all()
            print("All tables dropped")

            # Create all tables
            print("Creating all tables...")
            db.create_all()
            print("All tables created")

            # Check the schema of the client_data table
            print("\nChecking client_data table schema:")
            inspector = inspect(db.engine)
            for column in inspector.get_columns('client_data'):
                print(f"Column: {column['name']}, Type: {column['type']}")

            print("\nDatabase reset completed successfully!")
        except Exception as e:
            print(f"Error resetting database: {e}")

if __name__ == "__main__":
    main()
