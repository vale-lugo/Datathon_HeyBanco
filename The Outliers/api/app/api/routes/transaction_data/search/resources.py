from flask import request
from flask_jwt_extended import current_user
from flask_restx import Resource, marshal
from sqlalchemy import or_, and_

from app.api.routes.transaction_data.models import transaction_data_namespace
from app.api.routes.transaction_data.search.models import *
from app.models import TransactionData, ClientData
from app.utils.validations import authentication_required

@transaction_data_namespace.route('/search')
class SearchResource(Resource):
    @transaction_data_namespace.doc(
        description=get_search_description,
        params={
            'start_date': 'Start date for filtering (YYYY-MM-DD)',
            'end_date': 'End date for filtering (YYYY-MM-DD)',
            'min_amount': 'Minimum transaction amount',
            'max_amount': 'Maximum transaction amount',
            'merchant': 'Merchant name (partial match)',
            'category': 'Transaction category (partial match)',
            'type': 'Transaction type (exact match)',
            'page': 'Page number for pagination (default: 1)',
            'per_page': 'Number of results per page (default: 10, max: 100)'
        }
    )
    @transaction_data_namespace.response(
        code=200,
        model=get_search_response_model,
        description="Search results retrieved successfully"
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
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)
        merchant = request.args.get('merchant')
        category = request.args.get('category')
        transaction_type = request.args.get('type')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Limit per_page to a reasonable value
        if per_page > 100:
            per_page = 100

        # Build query
        query = TransactionData.query.filter_by(client_id=client_data.id)
        
        # Track applied filters
        filters_applied = {}
        
        # Apply date filters if provided
        if start_date:
            query = query.filter(TransactionData.fecha >= start_date)
            filters_applied['start_date'] = start_date
        if end_date:
            query = query.filter(TransactionData.fecha <= end_date)
            filters_applied['end_date'] = end_date
            
        # Apply amount filters if provided
        if min_amount is not None:
            query = query.filter(TransactionData.monto >= min_amount)
            filters_applied['min_amount'] = min_amount
        if max_amount is not None:
            query = query.filter(TransactionData.monto <= max_amount)
            filters_applied['max_amount'] = max_amount
            
        # Apply merchant filter if provided
        if merchant:
            query = query.filter(TransactionData.comercio.ilike(f'%{merchant}%'))
            filters_applied['merchant'] = merchant
            
        # Apply category filter if provided
        if category:
            query = query.filter(TransactionData.giro_comercio.ilike(f'%{category}%'))
            filters_applied['category'] = category
            
        # Apply transaction type filter if provided
        if transaction_type:
            query = query.filter(TransactionData.tipo_venta == transaction_type)
            filters_applied['type'] = transaction_type
            
        # Get total count
        total = query.count()
        
        # Apply pagination
        transactions = query.order_by(TransactionData.fecha.desc()).paginate(page=page, per_page=per_page, error_out=False)

        if not transactions.items and page > 1 and total > 0:
            response = {
                'error': 'Page not found'
            }
            response_data = marshal(
                response,
                resource_not_found_model
            )
            return response_data, 404

        # Create response
        transaction_list = []
        for transaction in transactions.items:
            transaction_list.append({
                'id': transaction.id,
                'fecha': transaction.fecha.isoformat() if transaction.fecha else None,
                'comercio': transaction.comercio,
                'giro_comercio': transaction.giro_comercio,
                'tipo_venta': transaction.tipo_venta,
                'monto': transaction.monto,
                'client_id': transaction.client_id
            })

        response = {
            'transactions': transaction_list,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': transactions.pages,
            'filters_applied': filters_applied
        }

        response_data = marshal(
            response,
            get_search_response_model
        )

        return response_data, 200