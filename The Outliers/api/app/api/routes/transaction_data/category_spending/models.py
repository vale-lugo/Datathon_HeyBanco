from flask_restx import fields
from app.api.routes.transaction_data.models import transaction_data_namespace, not_authenticated_model, resource_not_found_model

__all__ = [
    'get_category_spending_description',
    'get_category_spending_response_model',
    'category_spending_model',
    'not_authenticated_model',
    'resource_not_found_model'
]

# Define request descriptions
get_category_spending_description = (
    'Get spending by category for the authenticated user. '
    'Requires authentication. '
    'Returns a breakdown of spending by category, including total amount, '
    'percentage of total spending, and number of transactions.'
)

# Define category spending model
category_spending_model = transaction_data_namespace.model(
    name='CategorySpending',
    model={
        'category': fields.String(
            description='Spending category',
            example='SUPERMERCADO'
        ),
        'total_amount': fields.Float(
            description='Total amount spent in this category',
            example=1250.50
        ),
        'percentage': fields.Float(
            description='Percentage of total spending',
            example=23.68
        ),
        'transaction_count': fields.Integer(
            description='Number of transactions in this category',
            example=15
        ),
        'average_amount': fields.Float(
            description='Average transaction amount in this category',
            example=83.37
        )
    }
)

# Define category spending response model
get_category_spending_response_model = transaction_data_namespace.model(
    name='CategorySpendingGet',
    model={
        'categories': fields.List(
            fields.Nested(category_spending_model)
        ),
        'total_amount': fields.Float(
            description='Total amount spent across all categories',
            example=5280.75
        ),
        'total_transactions': fields.Integer(
            description='Total number of transactions',
            example=42
        ),
        'time_period': fields.String(
            description='Time period for the report',
            example='2023-01-01 to 2023-12-31'
        )
    }
)