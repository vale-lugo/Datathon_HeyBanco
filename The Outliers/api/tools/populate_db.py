import os
import csv
from datetime import datetime
from app import create_app, db
from app.models.client_data import ClientData
from app.models.transaction_data import TransactionData

def parse_date(date_str):
    """Parse date string to datetime object."""
    if not date_str or date_str.strip() == '':
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

def load_client_data(csv_path):
    """Load client data from CSV file into database."""
    print(f"Loading client data from {csv_path}...")

    # Count total rows
    with open(csv_path, 'r') as f:
        total_rows = sum(1 for _ in f) - 1  # Subtract 1 for header

    print(f"Found {total_rows} client records")

    # Process each row
    count = 0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check if client already exists
            client = ClientData.query.get(row['id'])
            if client is None:
                # Create new client
                client = ClientData(
                    id=row['id'],
                    fecha_nacimiento=parse_date(row['fecha_nacimiento']),
                    fecha_alta=parse_date(row['fecha_alta']),
                    id_municipio=int(row['id_municipio']) if row['id_municipio'] and row['id_municipio'].strip() else None,
                    id_estado=int(row['id_estado']) if row['id_estado'] and row['id_estado'].strip() else None,
                    tipo_persona=row['tipo_persona'] if row['tipo_persona'] and row['tipo_persona'].strip() else None,
                    genero=row['genero'] if row['genero'] and row['genero'].strip() else None,
                    actividad_empresarial=row['actividad_empresarial'] if row['actividad_empresarial'] and row['actividad_empresarial'].strip() else None
                )
                db.session.add(client)
                count += 1

                # Commit every 100 records to avoid memory issues
                if count % 100 == 0:
                    db.session.commit()
                    print(f"Processed {count}/{total_rows} client records")

    # Commit any remaining records
    db.session.commit()
    print(f"Successfully loaded {count} client records")

def load_transaction_data(csv_path):
    """Load transaction data from CSV file into database."""
    print(f"Loading transaction data from {csv_path}...")

    # Count total rows
    with open(csv_path, 'r') as f:
        total_rows = sum(1 for _ in f) - 1  # Subtract 1 for header

    print(f"Found {total_rows} transaction records")

    # Check if transactions are already loaded
    existing_count = TransactionData.query.count()
    if existing_count > 0:
        print(f"Found {existing_count} existing transaction records in database")
        print("Skipping transaction data loading to avoid duplicates")
        return

    # Process each row
    count = 0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create new transaction
            transaction = TransactionData(
                fecha=parse_date(row['fecha']),
                comercio=row['comercio'] if row['comercio'] and row['comercio'].strip() else None,
                giro_comercio=row['giro_comercio'] if row['giro_comercio'] and row['giro_comercio'].strip() else None,
                tipo_venta=row['tipo_venta'] if row['tipo_venta'] and row['tipo_venta'].strip() else None,
                monto=float(row['monto']) if row['monto'] and row['monto'].strip() else None,
                client_id=row['id']
            )
            db.session.add(transaction)
            count += 1

            # Commit every 100 records to avoid memory issues
            if count % 100 == 0:
                db.session.commit()
                print(f"Processed {count}/{total_rows} transaction records")

    # Commit any remaining records
    db.session.commit()
    print(f"Successfully loaded {count} transaction records")

def main():
    """Main function to load data into database."""
    # Create Flask app
    app = create_app()

    # Define paths to CSV files
    client_csv_path = os.path.join('data', 'raw', 'base_clientes_final.csv')
    transaction_csv_path = os.path.join('data', 'raw', 'base_transacciones_final.csv')

    # Check if CSV files exist
    if not os.path.exists(client_csv_path):
        print(f"Error: Client CSV file not found at {client_csv_path}")
        return

    if not os.path.exists(transaction_csv_path):
        print(f"Error: Transaction CSV file not found at {transaction_csv_path}")
        return

    # Load data into database
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Load client data
        load_client_data(client_csv_path)

        # Load transaction data
        load_transaction_data(transaction_csv_path)

    print("Data loading completed successfully!")

if __name__ == "__main__":
    main()
