from flask import Blueprint
from flask_restx import Namespace
from flask_restx import fields

__all__ = [
	'auth_namespace',
	'post_auth_login_description',
	'get_auth_me_description',
	'post_auth_logout_description',
	'post_auth_register_description',
	'post_auth_login_parser',
	'post_auth_login_request_model',
	'post_auth_login_response_model',
	'post_auth_register_parser',
	'post_auth_register_request_model',
	'post_auth_register_response_model',
	'get_auth_me_response_model',
	'bad_request_model',
	'resource_not_found_model',
	'unauthorized_model',
	'not_authenticated_model'
]

# Create authentication blueprint
auth_blueprint = Blueprint(
	name='authentication',
	import_name=__name__
)

# Create authentication namespace
auth_namespace = Namespace(
	name='Authentication',
	description='Authentication operations',
	path='/authentication'
)

# Define request descriptions
post_auth_login_description = (
	'Login user.'
)
get_auth_me_description = (
	'Get current user data with token information.'
	'Requires authentication.'
)
post_auth_logout_description = (
	'Logout user and invalidate token.'
)
post_auth_register_description = (
	'Register a new user.'
)

# Define request parsers
post_auth_login_parser = auth_namespace.parser()
post_auth_login_parser.add_argument(
	name='username',
	type=str,
	required=True,
	help='Username',
	location='json'
)
post_auth_login_parser.add_argument(
	name='password',
	type=str,
	required=True,
	help='Password',
	location='json'
)

post_auth_register_parser = auth_namespace.parser()
post_auth_register_parser.add_argument(
	name='username',
	type=str,
	required=True,
	help='Username',
	location='json'
)
post_auth_register_parser.add_argument(
	name='password',
	type=str,
	required=True,
	help='Password',
	location='json'
)
post_auth_register_parser.add_argument(
	name='client_id',
	type=str,
	required=False,
	help='Client ID',
	location='json'
)

# Define request models
post_auth_login_request_model = auth_namespace.model(
	name='AuthLoginPostRequest',
	model={
		'username': fields.String(
			required=True,
			example='username (required)',
			description='Login username (required)'
		),
		'password': fields.String(
			required=True,
			example='password (required)',
			description='Login password (required)'
		)
	}
)

post_auth_register_request_model = auth_namespace.model(
	name='AuthRegisterPostRequest',
	model={
		'username': fields.String(
			required=True,
			example='username (required)',
			description='Username for registration (required)'
		),
		'password': fields.String(
			required=True,
			example='password (required)',
			description='Password for registration (required)'
		),
		'client_id': fields.String(
			required=False,
			example='client123',
			description='Client ID (optional)'
		)
	}
)

# Define response models
post_auth_login_response_model = auth_namespace.model(
	name='AuthLoginPost',
	model={
		'access_token': fields.String(
			description='Access token',
			example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
		),
		'message': fields.String(
			description='Message',
			example='Login successful'
		),
		'issued_at': fields.String(
			description='Issued at',
			example='2020-01-01T00:00:00'
		),
		'expires_at': fields.String(
			description='Expires at',
			example='2020-01-01T00:00:00'
		)
	}
)

# Define user response model
user_response_model = auth_namespace.model(
	name='UserResponse',
	model={
		'id': fields.Integer(
			description='User ID',
			example=1
		),
		'username': fields.String(
			description='Username',
			example='username'
		),
		'client_id': fields.String(
			description='Client ID',
			example='client123'
		)
	}
)

get_auth_me_response_model = auth_namespace.model(
	name='AuthMeGet',
	model={
		'user': fields.Nested(user_response_model),
		'issued_at': fields.String(
			description='Issued at',
			example='2020-01-01T00:00:00'
		),
		'expires_at': fields.String(
			description='Expires at',
			example='2020-01-01T00:00:00'
		)
	}
)

post_auth_register_response_model = auth_namespace.model(
	name='AuthRegisterPost',
	model={
		'user': fields.Nested(user_response_model),
		'message': fields.String(
			description='Message',
			example='Registration successful'
		),
		'access_token': fields.String(
			description='Access token',
			example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
		),
		'issued_at': fields.String(
			description='Issued at',
			example='2020-01-01T00:00:00'
		),
		'expires_at': fields.String(
			description='Expires at',
			example='2020-01-01T00:00:00'
		)
	}
)

# Define error models
bad_request_model = auth_namespace.model(
	name='BadRequest',
	model={
		'error': fields.String(
			description='Error message',
			example='Bad request'
		)
	}
)

resource_not_found_model = auth_namespace.model(
	name='ResourceNotFound',
	model={
		'error': fields.String(
			description='Error message',
			example='Resource not found'
		)
	}
)

unauthorized_model = auth_namespace.model(
	name='Unauthorized',
	model={
		'error': fields.String(
			description='Error message',
			example='Unauthorized'
		)
	}
)

not_authenticated_model = auth_namespace.model(
	name='NotAuthenticated',
	model={
		'error': fields.String(
			description='Error message',
			example='Not authenticated'
		)
	}
)
