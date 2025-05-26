from flask_restx import fields
from app.api.routes.transaction_data.models import transaction_data_namespace, not_authenticated_model, resource_not_found_model

__all__ = [
    'get_statistics_description',
    'get_statistics_response_model',
    'not_authenticated_model',
    'resource_not_found_model'
]

# Define request descriptions
get_statistics_description = (
    'Get transaction statistics for the authenticated user. '
    'Requires authentication. '
    'Returns various statistics about the user\'s transaction history, '
    'including spending trends, average transaction amounts, and more.'
)

# Define statistics models
spending_trend_model = transaction_data_namespace.model(
    name='SpendingTrend',
    model={
        'period': fields.String(
            description='Time period (month or week)',
            example='2023-01'
        ),
        'amount': fields.Float(
            description='Total amount spent in the period',
            example=1250.50
        ),
        'transaction_count': fields.Integer(
            description='Number of transactions in the period',
            example=15
        ),
        'change_percentage': fields.Float(
            description='Percentage change from previous period',
            example=5.2
        )
    }
)

merchant_stat_model = transaction_data_namespace.model(
    name='MerchantStat',
    model={
        'merchant': fields.String(
            description='Merchant name',
            example='WALMART'
        ),
        'visit_count': fields.Integer(
            description='Number of visits/transactions',
            example=8
        ),
        'total_spent': fields.Float(
            description='Total amount spent at this merchant',
            example=450.75
        ),
        'average_transaction': fields.Float(
            description='Average transaction amount',
            example=56.34
        ),
        'last_visit': fields.String(
            description='Date of last visit',
            example='2023-01-15'
        )
    }
)

day_of_week_stat_model = transaction_data_namespace.model(
    name='DayOfWeekStat',
    model={
        'day': fields.String(
            description='Day of week',
            example='Monday'
        ),
        'transaction_count': fields.Integer(
            description='Number of transactions on this day',
            example=12
        ),
        'total_amount': fields.Float(
            description='Total amount spent on this day',
            example=580.25
        ),
        'average_amount': fields.Float(
            description='Average transaction amount on this day',
            example=48.35
        )
    }
)

# Define statistics response model
get_statistics_response_model = transaction_data_namespace.model(
    name='StatisticsGet',
    model={
        'summary': fields.Raw(
            description='Summary statistics',
            example={
                'total_transactions': 156,
                'total_spent': 8750.50,
                'average_transaction': 56.09,
                'highest_transaction': 350.00,
                'lowest_transaction': 5.25,
                'most_expensive_category': 'ELECTRONICS',
                'most_frequent_category': 'GROCERIES'
            }
        ),
        'spending_trends': fields.List(
            fields.Nested(spending_trend_model),
            description='Spending trends over time'
        ),
        'top_merchants': fields.List(
            fields.Nested(merchant_stat_model),
            description='Statistics for most visited merchants'
        ),
        'day_of_week_stats': fields.List(
            fields.Nested(day_of_week_stat_model),
            description='Spending patterns by day of week'
        ),
        'time_period': fields.String(
            description='Time period for the statistics',
            example='Last 12 months'
        )
    }
)