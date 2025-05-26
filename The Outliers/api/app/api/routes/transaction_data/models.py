from flask import Blueprint
from flask_restx import Namespace
from flask_restx import fields

__all__ = [
	'transaction_data_namespace',
	'get_transaction_data_description',
	'get_transaction_data_response_model',
	'bad_request_model',
	'resource_not_found_model',
	'unauthorized_model',
	'not_authenticated_model'
]

# Create transaction data blueprint
transaction_data_blueprint = Blueprint(
	name='transaction_data',
	import_name=__name__
)

# Create transaction data namespace
transaction_data_namespace = Namespace(
	name='TransactionData',
	description='Transaction data operations',
	path='/transaction_data'
)

# Define request descriptions
get_transaction_data_description = (
	'Get transaction data for the authenticated user.'
	'Requires authentication.'
)

# Define transaction data response model
transaction_data_response_model = transaction_data_namespace.model(
	name='TransactionDataResponse',
	model={
		'id': fields.Integer(
			description='Transaction ID',
			example=1
		),
		'fecha': fields.String(
			description='Transaction date',
			example='2020-01-01'
		),
		'comercio': fields.String(
			description='Commerce',
			example='WALMART'
		),
		'giro_comercio': fields.String(
			description='Commerce type',
			example='SUPERMERCADO'
		),
		'tipo_venta': fields.String(
			description='Sale type',
			example='ONLINE'
		),
		'monto': fields.Float(
			description='Amount',
			example=100.50
		),
		'client_id': fields.String(
			description='Client ID',
			example='client123'
		)
	}
)

get_transaction_data_response_model = transaction_data_namespace.model(
	name='TransactionDataGet',
	model={
		'transactions': fields.List(
			fields.Nested(transaction_data_response_model)
		),
		'total': fields.Integer(
			description='Total number of transactions',
			example=10
		)
	}
)

# Define error models
bad_request_model = transaction_data_namespace.model(
	name='BadRequest',
	model={
		'error': fields.String(
			description='Error message',
			example='Bad request'
		)
	}
)

resource_not_found_model = transaction_data_namespace.model(
	name='ResourceNotFound',
	model={
		'error': fields.String(
			description='Error message',
			example='Resource not found'
		)
	}
)

unauthorized_model = transaction_data_namespace.model(
	name='Unauthorized',
	model={
		'error': fields.String(
			description='Error message',
			example='Unauthorized'
		)
	}
)

not_authenticated_model = transaction_data_namespace.model(
	name='NotAuthenticated',
	model={
		'error': fields.String(
			description='Error message',
			example='Not authenticated'
		)
	}
)
