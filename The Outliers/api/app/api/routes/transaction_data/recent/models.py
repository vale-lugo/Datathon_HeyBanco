from flask_restx import fields
from app.api.routes.transaction_data.models import transaction_data_namespace, transaction_data_response_model, not_authenticated_model, resource_not_found_model

__all__ = [
    'get_recent_transactions_description',
    'get_recent_transactions_response_model',
    'not_authenticated_model',
    'resource_not_found_model'
]

# Define request descriptions
get_recent_transactions_description = (
    'Get recent transactions for the authenticated user. '
    'Requires authentication. '
    'Returns the most recent transactions, with optional limit parameter.'
)

# Define recent transactions response model
get_recent_transactions_response_model = transaction_data_namespace.model(
    name='RecentTransactionsGet',
    model={
        'transactions': fields.List(
            fields.Nested(transaction_data_response_model)
        ),
        'total': fields.Integer(
            description='Total number of transactions returned',
            example=10
        ),
        'limit': fields.Integer(
            description='Maximum number of transactions requested',
            example=10
        ),
        'last_updated': fields.String(
            description='Timestamp of the most recent transaction',
            example='2023-12-31T23:59:59'
        )
    }
)