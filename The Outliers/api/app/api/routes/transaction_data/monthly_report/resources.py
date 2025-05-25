from flask import request
from flask_jwt_extended import current_user
from flask_restx import Resource, marshal
from sqlalchemy import func, extract, desc
from collections import defaultdict

from app.api.routes.transaction_data.models import transaction_data_namespace
from app.api.routes.transaction_data.monthly_report.models import *
from app.models import TransactionData, ClientData
from app.utils.validations import authentication_required

@transaction_data_namespace.route('/monthly_report')
class MonthlyReportResource(Resource):
    @transaction_data_namespace.doc(
        description=get_monthly_report_description
    )
    @transaction_data_namespace.response(
        code=200,
        model=get_monthly_report_response_model,
        description="Monthly report generated successfully"
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
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 12, type=int)  # Default to 12 months

        # Build query
        query = TransactionData.query.filter_by(client_id=client_data.id)

        # Apply date filters if provided
        if start_date:
            query = query.filter(TransactionData.fecha >= start_date)
        if end_date:
            query = query.filter(TransactionData.fecha <= end_date)

        # Get all transactions
        transactions = query.all()

        # Group transactions by month
        monthly_data = defaultdict(lambda: {
            'transactions': [],
            'total_amount': 0,
            'transaction_count': 0,
            'categories': defaultdict(float)
        })

        for transaction in transactions:
            if transaction.fecha:
                month_key = transaction.fecha.strftime('%Y-%m')
                monthly_data[month_key]['transactions'].append(transaction)
                monthly_data[month_key]['total_amount'] += transaction.monto if transaction.monto else 0
                monthly_data[month_key]['transaction_count'] += 1

                # Track spending by category
                if transaction.giro_comercio and transaction.monto:
                    monthly_data[month_key]['categories'][transaction.giro_comercio] += transaction.monto

        # Sort months by date (newest first) and limit to requested number
        sorted_months = sorted(monthly_data.keys(), reverse=True)[:limit]

        # Build response
        monthly_summaries = []
        for month in sorted_months:
            data = monthly_data[month]

            # Calculate average amount
            average_amount = data['total_amount'] / data['transaction_count'] if data['transaction_count'] > 0 else 0

            # Get top categories
            top_categories = []
            if data['total_amount'] > 0:
                # Sort categories by amount spent
                sorted_categories = sorted(
                    data['categories'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:5]  # Top 5 categories

                for category, amount in sorted_categories:
                    percentage = (amount / data['total_amount']) * 100
                    top_categories.append({
                        'category': category,
                        'amount': amount,
                        'percentage': round(percentage, 2)
                    })

            monthly_summaries.append({
                'month': month,
                'total_amount': round(data['total_amount'], 2),
                'transaction_count': data['transaction_count'],
                'average_amount': round(average_amount, 2),
                'top_categories': top_categories
            })

        response = {
            'monthly_summaries': monthly_summaries,
            'total_months': len(monthly_summaries)
        }

        response_data = marshal(
            response,
            get_monthly_report_response_model
        )

        return response_data, 200
