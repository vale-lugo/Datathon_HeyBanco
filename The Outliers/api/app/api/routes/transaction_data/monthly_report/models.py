from flask_restx import fields
from app.api.routes.transaction_data.models import transaction_data_namespace, not_authenticated_model, resource_not_found_model

__all__ = [
    'get_monthly_report_description',
    'get_monthly_report_response_model',
    'monthly_summary_model',
    'not_authenticated_model',
    'resource_not_found_model'
]

# Define request descriptions
get_monthly_report_description = (
    'Get monthly transaction report for the authenticated user. '
    'Requires authentication. '
    'Returns a summary of transactions grouped by month, including total amount, '
    'number of transactions, average transaction amount, and top spending categories.'
)

# Define monthly summary model
monthly_summary_model = transaction_data_namespace.model(
    name='MonthlySummary',
    model={
        'month': fields.String(
            description='Month (YYYY-MM)',
            example='2023-01'
        ),
        'total_amount': fields.Float(
            description='Total amount spent in the month',
            example=5280.75
        ),
        'transaction_count': fields.Integer(
            description='Number of transactions in the month',
            example=42
        ),
        'average_amount': fields.Float(
            description='Average transaction amount',
            example=125.73
        ),
        'top_categories': fields.List(
            fields.Nested(
                transaction_data_namespace.model(
                    'TopCategory',
                    {
                        'category': fields.String(
                            description='Spending category',
                            example='SUPERMERCADO'
                        ),
                        'amount': fields.Float(
                            description='Total amount spent in this category',
                            example=1250.50
                        ),
                        'percentage': fields.Float(
                            description='Percentage of total spending',
                            example=23.68
                        )
                    }
                )
            ),
            description='Top spending categories for the month',
            example=[
                {'category': 'SUPERMERCADO', 'amount': 1250.50, 'percentage': 23.68},
                {'category': 'RESTAURANTE', 'amount': 850.25, 'percentage': 16.10},
                {'category': 'TRANSPORTE', 'amount': 520.00, 'percentage': 9.85}
            ]
        )
    }
)

# Define monthly report response model
get_monthly_report_response_model = transaction_data_namespace.model(
    name='MonthlyReportGet',
    model={
        'monthly_summaries': fields.List(
            fields.Nested(monthly_summary_model)
        ),
        'total_months': fields.Integer(
            description='Total number of months with transactions',
            example=12
        )
    }
)