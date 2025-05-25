from flask import request
from flask_jwt_extended import current_user
from flask_restx import Resource, marshal
from collections import defaultdict
from datetime import datetime

from app.api.routes.transaction_data.models import transaction_data_namespace
from app.api.routes.transaction_data.category_spending.models import *
from app.models import TransactionData, ClientData
from app.utils.validations import authentication_required

@transaction_data_namespace.route('/category_spending')
class CategorySpendingResource(Resource):
    @transaction_data_namespace.doc(
        description=get_category_spending_description
    )
    @transaction_data_namespace.response(
        code=200,
        model=get_category_spending_response_model,
        description="Category spending report generated successfully"
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

        # Build query
        query = TransactionData.query.filter_by(client_id=client_data.id)

        # Apply date filters if provided
        if start_date:
            query = query.filter(TransactionData.fecha >= start_date)
        if end_date:
            query = query.filter(TransactionData.fecha <= end_date)

        # Get all transactions
        transactions = query.all()

        # Initialize variables for tracking
        total_amount = 0
        total_transactions = 0
        category_data = defaultdict(lambda: {
            'total_amount': 0,
            'transaction_count': 0
        })

        # Process transactions
        for transaction in transactions:
            if transaction.monto:
                total_amount += transaction.monto
                total_transactions += 1

                # Group by category (giro_comercio)
                category = transaction.giro_comercio or 'UNCATEGORIZED'
                category_data[category]['total_amount'] += transaction.monto
                category_data[category]['transaction_count'] += 1

        # Build response
        categories = []
        for category, data in category_data.items():
            # Calculate percentage and average
            percentage = (data['total_amount'] / total_amount * 100) if total_amount > 0 else 0
            average = data['total_amount'] / data['transaction_count'] if data['transaction_count'] > 0 else 0

            categories.append({
                'category': category,
                'total_amount': round(data['total_amount'], 2),
                'percentage': round(percentage, 2),
                'transaction_count': data['transaction_count'],
                'average_amount': round(average, 2)
            })

        # Sort categories by total amount (highest first)
        categories.sort(key=lambda x: x['total_amount'], reverse=True)

        # Determine time period string
        time_period = "All time"
        if start_date and end_date:
            time_period = f"{start_date} to {end_date}"
        elif start_date:
            time_period = f"From {start_date}"
        elif end_date:
            time_period = f"Until {end_date}"

        response = {
            'categories': categories,
            'total_amount': round(total_amount, 2),
            'total_transactions': total_transactions,
            'time_period': time_period
        }

        response_data = marshal(
            response,
            get_category_spending_response_model
        )

        return response_data, 200
