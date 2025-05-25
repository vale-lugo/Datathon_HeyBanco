from flask import Blueprint
from flask_restx import Namespace
from flask_restx import fields

__all__ = [
	'client_data_namespace',
	'get_client_data_description',
	'get_client_data_response_model',
	'bad_request_model',
	'resource_not_found_model',
	'unauthorized_model',
	'not_authenticated_model'
]

# Create client data blueprint
client_data_blueprint = Blueprint(
	name='client_data',
	import_name=__name__
)

# Create client data namespace
client_data_namespace = Namespace(
	name='ClientData',
	description='Client data operations',
	path='/client_data'
)

# Define request descriptions
get_client_data_description = (
	'Get client data for the authenticated user.'
	'Requires authentication.'
)

# Define client data response model
client_data_response_model = client_data_namespace.model(
	name='ClientDataResponse',
	model={
		'id': fields.String(
			description='Client ID',
			example='client123'
		),
		'fecha_nacimiento': fields.String(
			description='Birth date',
			example='1990-01-01'
		),
		'fecha_alta': fields.String(
			description='Registration date',
			example='2020-01-01'
		),
		'id_municipio': fields.Integer(
			description='Municipality ID',
			example=1
		),
		'id_estado': fields.Integer(
			description='State ID',
			example=1
		),
		'tipo_persona': fields.String(
			description='Person type',
			example='FISICA'
		),
		'genero': fields.String(
			description='Gender',
			example='M'
		),
		'actividad_empresarial': fields.String(
			description='Business activity',
			example='COMERCIO'
		)
	}
)

get_client_data_response_model = client_data_namespace.model(
	name='ClientDataGet',
	model={
		'client_data': fields.Nested(client_data_response_model)
	}
)

# Define error models
bad_request_model = client_data_namespace.model(
	name='BadRequest',
	model={
		'error': fields.String(
			description='Error message',
			example='Bad request'
		)
	}
)

resource_not_found_model = client_data_namespace.model(
	name='ResourceNotFound',
	model={
		'error': fields.String(
			description='Error message',
			example='Resource not found'
		)
	}
)

unauthorized_model = client_data_namespace.model(
	name='Unauthorized',
	model={
		'error': fields.String(
			description='Error message',
			example='Unauthorized'
		)
	}
)

not_authenticated_model = client_data_namespace.model(
	name='NotAuthenticated',
	model={
		'error': fields.String(
			description='Error message',
			example='Not authenticated'
		)
	}
)
