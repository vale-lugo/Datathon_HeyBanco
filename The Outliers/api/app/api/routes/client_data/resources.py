from flask import jsonify
from flask_jwt_extended import (
	jwt_required,
	current_user
)
from flask_restx import (
	Resource,
	marshal
)

from app.api.routes.client_data.models import *
from app.models import ClientData
from app.utils.validations import authentication_required


@client_data_namespace.route('')
class ClientDataResource(Resource):
	@client_data_namespace.doc(
		description=get_client_data_description
	)
	@client_data_namespace.response(
		code=200,
		model=get_client_data_response_model,
		description="Client data found"
	)
	@client_data_namespace.response(
		code=401,
		model=not_authenticated_model,
		description="Not authenticated"
	)
	@client_data_namespace.response(
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

		# Create response
		response = {
			'client_data': {
				'id': client_data.id,
				'fecha_nacimiento': client_data.fecha_nacimiento.isoformat() if client_data.fecha_nacimiento else None,
				'fecha_alta': client_data.fecha_alta.isoformat() if client_data.fecha_alta else None,
				'id_municipio': client_data.id_municipio,
				'id_estado': client_data.id_estado,
				'tipo_persona': client_data.tipo_persona,
				'genero': client_data.genero,
				'actividad_empresarial': client_data.actividad_empresarial
			}
		}

		response_data = marshal(
			response,
			get_client_data_response_model
		)

		return response_data, 200