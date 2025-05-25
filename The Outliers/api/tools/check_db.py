from app import create_app, db
from app.models.client_data import ClientData
from app.models.transaction_data import TransactionData

def main():
    app = create_app()
    
    with app.app_context():
        # Check client data
        client_count = ClientData.query.count()
        print(f"Number of client records in database: {client_count}")
        
        # Check transaction data
        transaction_count = TransactionData.query.count()
        print(f"Number of transaction records in database: {transaction_count}")
        
        # Check a few sample records if available
        if client_count > 0:
            print("\nSample client record:")
            client = ClientData.query.first()
            print(f"ID: {client.id}")
            print(f"Tipo Persona: {client.tipo_persona}")
            print(f"Genero: {client.genero}")
            
        if transaction_count > 0:
            print("\nSample transaction record:")
            transaction = TransactionData.query.first()
            print(f"ID: {transaction.id}")
            print(f"Client ID: {transaction.client_id}")
            print(f"Monto: {transaction.monto}")
            print(f"Comercio: {transaction.comercio}")

if __name__ == "__main__":
    main()