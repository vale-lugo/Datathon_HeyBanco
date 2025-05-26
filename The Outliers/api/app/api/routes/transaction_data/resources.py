from flask import jsonify, request
from flask_jwt_extended import (
	jwt_required,
	current_user
)
from flask_restx import (
	Resource,
	marshal
)

from app.api.routes.transaction_data.models import *
from app.models import TransactionData, ClientData
from app.utils.validations import authentication_required


@transaction_data_namespace.route('')
class TransactionDataResource(Resource):
	@transaction_data_namespace.doc(
		description=get_transaction_data_description
	)
	@transaction_data_namespace.response(
		code=200,
		model=get_transaction_data_response_model,
		description="Transaction data found"
	)
	@transaction_data_namespace.response(
		code=401,
		model=not_authenticated_model,
		description="Not authenticated"
	)
	@transaction_data_namespace.response(
		code=404,
		model=resource_not_found_model,
		description="Transaction data not found"
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

		# Get query parameters for pagination
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', 10, type=int)

		# Limit per_page to a reasonable value
		if per_page > 100:
			per_page = 100

		# Get transaction data for the client
		transactions_query = TransactionData.query.filter_by(client_id=client_data.id)
		
		# Get total count
		total = transactions_query.count()
		
		# Apply pagination
		transactions = transactions_query.paginate(page=page, per_page=per_page, error_out=False)

		if not transactions.items and page > 1:
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
			'total': total
		}

		response_data = marshal(
			response,
			get_transaction_data_response_model
		)

		return response_data, 200