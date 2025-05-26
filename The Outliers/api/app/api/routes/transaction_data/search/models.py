from flask_restx import fields
from app.api.routes.transaction_data.models import transaction_data_namespace, transaction_data_response_model, not_authenticated_model, resource_not_found_model

__all__ = [
    'get_search_description',
    'get_search_response_model',
    'search_params_model',
    'not_authenticated_model',
    'resource_not_found_model'
]

# Define request descriptions
get_search_description = (
    'Search and filter transactions for the authenticated user. '
    'Requires authentication. '
    'Supports filtering by date range, amount range, merchant, category, and transaction type. '
    'Returns paginated results with matching transactions.'
)

# Define search parameters model for documentation
search_params_model = transaction_data_namespace.model(
    name='SearchParams',
    model={
        'start_date': fields.String(
            description='Start date for filtering (YYYY-MM-DD)',
            example='2023-01-01'
        ),
        'end_date': fields.String(
            description='End date for filtering (YYYY-MM-DD)',
            example='2023-12-31'
        ),
        'min_amount': fields.Float(
            description='Minimum transaction amount',
            example=10.0
        ),
        'max_amount': fields.Float(
            description='Maximum transaction amount',
            example=1000.0
        ),
        'merchant': fields.String(
            description='Merchant name (partial match)',
            example='WALMART'
        ),
        'category': fields.String(
            description='Transaction category (partial match)',
            example='SUPERMERCADO'
        ),
        'type': fields.String(
            description='Transaction type (exact match)',
            example='ONLINE'
        ),
        'page': fields.Integer(
            description='Page number for pagination',
            example=1
        ),
        'per_page': fields.Integer(
            description='Number of results per page',
            example=10
        )
    }
)

# Define search response model
get_search_response_model = transaction_data_namespace.model(
    name='SearchGet',
    model={
        'transactions': fields.List(
            fields.Nested(transaction_data_response_model)
        ),
        'total': fields.Integer(
            description='Total number of matching transactions',
            example=42
        ),
        'page': fields.Integer(
            description='Current page number',
            example=1
        ),
        'per_page': fields.Integer(
            description='Number of results per page',
            example=10
        ),
        'pages': fields.Integer(
            description='Total number of pages',
            example=5
        ),
        'filters_applied': fields.Raw(
            description='Filters that were applied to the search',
            example={
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'min_amount': 10.0,
                'max_amount': 1000.0,
                'merchant': 'WALMART',
                'category': 'SUPERMERCADO',
                'type': 'ONLINE'
            }
        )
    }
)