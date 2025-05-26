from flask import request
from flask_jwt_extended import current_user
from flask_restx import Resource, marshal
from datetime import datetime

from app.api.routes.transaction_data.models import transaction_data_namespace
from app.api.routes.transaction_data.recent.models import *
from app.models import TransactionData, ClientData
from app.utils.validations import authentication_required

@transaction_data_namespace.route('/recent')
class RecentTransactionsResource(Resource):
    @transaction_data_namespace.doc(
        description=get_recent_transactions_description,
        params={
            'limit': 'Maximum number of transactions to return (default: 10, max: 50)'
        }
    )
    @transaction_data_namespace.response(
        code=200,
        model=get_recent_transactions_response_model,
        description="Recent transactions retrieved successfully"
    )
    @transaction_data_namespace.response(
        code=401,
        model=not_authenticated_model,
        description="Not authenticated"
    )
    @transaction_data_namespace.response(
        code=404,
        model=resource_not_found_model,
        description="Client data not found"
    )
    @authentication_required(not_authenticated_model)
    def get(self):
        # Get client data for the authenticated user
        if not current_user.client_id:
            response = {
                'error': 'Client data not found for this user'
            }
            response_data = marshal(
                response,
                resource_not_found_model
            )
            return response_data, 404

        # Get client data
        client_data = ClientData.query.get(current_user.client_id)

        if not client_data:
            response = {
                'error': 'Client data not found'
            }
            response_data = marshal(
                response,
                resource_not_found_model
            )
            return response_data, 404

        # Get query parameters
        limit = request.args.get('limit', 10, type=int)
        
        # Limit to a reasonable value
        if limit > 50:
            limit = 50

        # Get recent transactions
        transactions = TransactionData.query.filter_by(client_id=client_data.id) \
            .order_by(TransactionData.fecha.desc()) \
            .limit(limit) \
            .all()

        # Create response
        transaction_list = []
        last_updated = None
        
        for transaction in transactions:
            transaction_list.append({
                'id': transaction.id,
                'fecha': transaction.fecha.isoformat() if transaction.fecha else None,
                'comercio': transaction.comercio,
                'giro_comercio': transaction.giro_comercio,
                'tipo_venta': transaction.tipo_venta,
                'monto': transaction.monto,
                'client_id': transaction.client_id
            })
            
            # Track the most recent transaction date
            if transaction.fecha and (last_updated is None or transaction.fecha > last_updated):
                last_updated = transaction.fecha

        response = {
            'transactions': transaction_list,
            'total': len(transaction_list),
            'limit': limit,
            'last_updated': last_updated.isoformat() if last_updated else None
        }

        response_data = marshal(
            response,
            get_recent_transactions_response_model
        )

        return response_data, 200