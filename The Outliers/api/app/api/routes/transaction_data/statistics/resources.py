from flask import request
from flask_jwt_extended import current_user
from flask_restx import Resource, marshal
from sqlalchemy import func, extract, desc
from collections import defaultdict
from datetime import datetime, timedelta
import calendar

from app.api.routes.transaction_data.models import transaction_data_namespace
from app.api.routes.transaction_data.statistics.models import *
from app.models import TransactionData, ClientData
from app.utils.validations import authentication_required

@transaction_data_namespace.route('/statistics')
class StatisticsResource(Resource):
    @transaction_data_namespace.doc(
        description=get_statistics_description,
        params={
            'months': 'Number of months to include in statistics (default: 12)'
        }
    )
    @transaction_data_namespace.response(
        code=200,
        model=get_statistics_response_model,
        description="Statistics generated successfully"
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
        months = request.args.get('months', 12, type=int)

        # Get all transactions for the client without date filtering
        transactions = TransactionData.query.filter_by(client_id=client_data.id).all()

        # Log the number of transactions found for debugging
        print(f"Found {len(transactions)} transactions for client {client_data.id}")

        if not transactions:
            # Return empty statistics if no transactions found
            response = {
                'summary': {
                    'total_transactions': 0,
                    'total_spent': 0,
                    'average_transaction': 0,
                    'highest_transaction': 0,
                    'lowest_transaction': 0,
                    'most_expensive_category': None,
                    'most_frequent_category': None
                },
                'spending_trends': [],
                'top_merchants': [],
                'day_of_week_stats': [],
                'time_period': f"Last {months} months"
            }

            response_data = marshal(
                response,
                get_statistics_response_model
            )

            return response_data, 200

        # Calculate summary statistics
        total_transactions = len(transactions)

        # Filter out transactions with None monto
        valid_transactions = [t for t in transactions if t.monto is not None]

        # Calculate statistics only if there are valid transactions
        if valid_transactions:
            total_spent = sum(t.monto for t in valid_transactions)
            average_transaction = total_spent / len(valid_transactions)
            highest_transaction = max(t.monto for t in valid_transactions)
            lowest_transaction = min(t.monto for t in valid_transactions)
        else:
            total_spent = 0
            average_transaction = 0
            highest_transaction = 0
            lowest_transaction = 0

        # Log summary statistics for debugging
        print(f"Total transactions: {total_transactions}")
        print(f"Valid transactions (with monto): {len(valid_transactions)}")
        print(f"Total spent: {total_spent}")
        print(f"Average transaction: {average_transaction}")
        print(f"Highest transaction: {highest_transaction}")
        print(f"Lowest transaction: {lowest_transaction}")

        # Calculate category statistics
        category_counts = defaultdict(int)
        category_amounts = defaultdict(float)

        for t in transactions:
            if t.giro_comercio and t.monto is not None:
                category_counts[t.giro_comercio] += 1
                category_amounts[t.giro_comercio] += t.monto

        # Only calculate most frequent/expensive if we have categories
        if category_counts:
            most_frequent_category = max(category_counts.items(), key=lambda x: x[1])[0]
            print(f"Most frequent category: {most_frequent_category} with {category_counts[most_frequent_category]} transactions")
        else:
            most_frequent_category = None
            print("No categories found for most frequent")

        if category_amounts:
            most_expensive_category = max(category_amounts.items(), key=lambda x: x[1])[0]
            print(f"Most expensive category: {most_expensive_category} with ${category_amounts[most_expensive_category]:.2f}")
        else:
            most_expensive_category = None
            print("No categories found for most expensive")

        # Calculate spending trends (monthly)
        monthly_data = defaultdict(lambda: {'amount': 0, 'count': 0})

        # Only process transactions with valid fecha and monto
        for t in transactions:
            if t.fecha and t.monto is not None:
                month_key = t.fecha.strftime('%Y-%m')
                monthly_data[month_key]['amount'] += t.monto
                monthly_data[month_key]['count'] += 1

        # Sort months chronologically
        sorted_months = sorted(monthly_data.keys())
        print(f"Found {len(sorted_months)} months with transaction data")

        # Calculate month-over-month changes
        spending_trends = []
        for i, month in enumerate(sorted_months):
            data = monthly_data[month]
            change_percentage = 0

            if i > 0:
                prev_month = sorted_months[i-1]
                prev_amount = monthly_data[prev_month]['amount']
                if prev_amount > 0:
                    change_percentage = ((data['amount'] - prev_amount) / prev_amount) * 100

            spending_trends.append({
                'period': month,
                'amount': round(data['amount'], 2),
                'transaction_count': data['count'],
                'change_percentage': round(change_percentage, 2)
            })

        print(f"Generated {len(spending_trends)} spending trend entries")

        # Calculate merchant statistics
        merchant_data = defaultdict(lambda: {
            'visit_count': 0, 
            'total_spent': 0, 
            'last_visit': None
        })

        # Only process transactions with valid comercio and monto
        for t in transactions:
            if t.comercio and t.monto is not None:
                merchant_data[t.comercio]['visit_count'] += 1
                merchant_data[t.comercio]['total_spent'] += t.monto

                if t.fecha and (merchant_data[t.comercio]['last_visit'] is None or 
                               t.fecha > merchant_data[t.comercio]['last_visit']):
                    merchant_data[t.comercio]['last_visit'] = t.fecha

        print(f"Found {len(merchant_data)} unique merchants")

        # Get top merchants by visit count
        top_merchants = []

        # Only process if we have merchant data
        if merchant_data:
            for merchant, data in sorted(merchant_data.items(), key=lambda x: x[1]['visit_count'], reverse=True)[:5]:
                average = data['total_spent'] / data['visit_count'] if data['visit_count'] > 0 else 0
                top_merchants.append({
                    'merchant': merchant,
                    'visit_count': data['visit_count'],
                    'total_spent': round(data['total_spent'], 2),
                    'average_transaction': round(average, 2),
                    'last_visit': data['last_visit'].isoformat() if data['last_visit'] else None
                })

        print(f"Generated {len(top_merchants)} top merchant entries")

        # Calculate day of week statistics
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_stats = defaultdict(lambda: {'count': 0, 'amount': 0})

        # Only process transactions with valid fecha and monto
        for t in transactions:
            if t.fecha and t.monto is not None:
                # Get day of week (0 = Monday, 6 = Sunday)
                day_idx = t.fecha.weekday()
                day_name = days_of_week[day_idx]

                day_stats[day_name]['count'] += 1
                day_stats[day_name]['amount'] += t.monto

        print(f"Found transactions on {len(day_stats)} different days of the week")

        # Build day of week stats
        day_of_week_stats = []

        # Process each day of the week
        for day in days_of_week:
            # Only include days that have data
            if day in day_stats:
                data = day_stats[day]
                average = data['amount'] / data['count'] if data['count'] > 0 else 0
                day_of_week_stats.append({
                    'day': day,
                    'transaction_count': data['count'],
                    'total_amount': round(data['amount'], 2),
                    'average_amount': round(average, 2)
                })

        print(f"Generated {len(day_of_week_stats)} day of week stat entries")

        # Build response
        response = {
            'summary': {
                'total_transactions': total_transactions,
                'total_spent': round(total_spent, 2),
                'average_transaction': round(average_transaction, 2),
                'highest_transaction': round(highest_transaction, 2),
                'lowest_transaction': round(lowest_transaction, 2),
                'most_expensive_category': most_expensive_category,
                'most_frequent_category': most_frequent_category
            },
            'spending_trends': spending_trends,
            'top_merchants': top_merchants,
            'day_of_week_stats': day_of_week_stats,
            'time_period': f"Last {months} months"
        }

        response_data = marshal(
            response,
            get_statistics_response_model
        )

        return response_data, 200
