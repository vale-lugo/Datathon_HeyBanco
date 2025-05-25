from uuid import UUID

from flask_jwt_extended import (
	jwt_required,
	get_jwt
)
from flask_restx import marshal

from app.utils import get_user_from_jwt


def validate_uuid(uuid_string):
	try:
		val = UUID(uuid_string, version=4)
	except ValueError:
		return False

	return str(val) == uuid_string


def authentication_required(not_authenticated_model):
	def decorator(func):
		@jwt_required()
		def wrapper(*args, **kwargs):
			user = get_user_from_jwt(jwt=get_jwt())
			if not user:
				response = {
					'error': 'Not authenticated'
				}
				response_data = marshal(response, not_authenticated_model)
				return response_data, 401
			return func(*args, **kwargs)

		return wrapper

	return decorator
