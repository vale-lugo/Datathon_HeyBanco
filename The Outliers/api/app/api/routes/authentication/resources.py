from flask import (
	make_response,
	jsonify
)
from flask_jwt_extended import (
	get_jwt,
	create_access_token,
	set_access_cookies,
	unset_jwt_cookies,
	jwt_required,
	decode_token
)
from flask_restx import (
	Resource,
	marshal
)

from app.api.routes.authentication.models import *
from app.models import User
from app import db
from app.utils import get_user_from_jwt
from app.utils.validations import authentication_required


@auth_namespace.route('/login')
class AuthLoginResource(Resource):
	@auth_namespace.doc(
		description=post_auth_login_description,
		order=1
	)
	@auth_namespace.expect(
		post_auth_login_request_model
	)
	@auth_namespace.response(
		code=200,
		model=post_auth_login_response_model,
		description="Login successful"
	)
	@auth_namespace.response(
		code=400,
		model=bad_request_model,
		description="Bad Request"
	)
	@auth_namespace.response(
		code=404,
		model=resource_not_found_model,
		description="Resource not found"
	)
	def post(self):
		# Get data from request
		data = post_auth_login_parser.parse_args()

		# Get user data
		username = data.get('username')
		password = data.get('password')

		# Check if user data is valid
		if not username:
			response = {
				'error': 'Missing username'
			}
			response_data = marshal(
				response,
				bad_request_model
			)
			return response_data, 400

		if not password:
			response = {
				'error': 'Missing password'
			}
			response_data = marshal(
				response,
				bad_request_model
			)
			return response_data, 400

		# Get user
		user = User.query.filter_by(username=username).first()

		# Check if user exists
		if not user:
			response = {
				'error': 'User not found'
			}
			response_data = marshal(
				response,
				resource_not_found_model
			)
			return response_data, 404

		# Check password
		if user.password != password:  # In a real app, use proper password hashing
			response = {
				'error': 'Invalid password'
			}
			response_data = marshal(
				response,
				bad_request_model
			)
			return response_data, 400

		# Return access token
		access_token = create_access_token(identity=str(user.id))
		decoded_token = decode_token(access_token)
		issued_at = decoded_token['iat']
		expires_at = decoded_token['exp']

		data = {
			'access_token': access_token,
			'message': 'Login successful',
			'issued_at': issued_at,
			'expires_at': expires_at
		}

		max_age = expires_at - issued_at

		response_data = marshal(
			data,
			post_auth_login_response_model
		)

		response = make_response(jsonify(response_data), 200)
		set_access_cookies(response, access_token, max_age=max_age)

		return response



@auth_namespace.route('/logout')
class AuthLogoutResource(Resource):
	@auth_namespace.doc(
		description=post_auth_logout_description,
		order=4
	)
	@auth_namespace.response(
		code=200,
		description="Logout successful"
	)
	@jwt_required(optional=True)
	def post(self):
		# Create response
		response_data = {
			'message': 'Logout successful'
		}

		# Create response object
		response = make_response(jsonify(response_data), 200)

		# Unset JWT cookies
		unset_jwt_cookies(response)

		return response


@auth_namespace.route('/register')
class AuthRegisterResource(Resource):
	@auth_namespace.doc(
		description=post_auth_register_description,
		order=2
	)
	@auth_namespace.expect(
		post_auth_register_request_model
	)
	@auth_namespace.response(
		code=201,
		model=post_auth_register_response_model,
		description="Registration successful"
	)
	@auth_namespace.response(
		code=400,
		model=bad_request_model,
		description="Bad Request"
	)
	def post(self):
		# Get data from request
		data = post_auth_register_parser.parse_args()

		# Get user data
		username = data.get('username')
		password = data.get('password')
		client_id = data.get('client_id')

		# Check if user data is valid
		if not username:
			response = {
				'error': 'Missing username'
			}
			response_data = marshal(
				response,
				bad_request_model
			)
			return response_data, 400

		if not password:
			response = {
				'error': 'Missing password'
			}
			response_data = marshal(
				response,
				bad_request_model
			)
			return response_data, 400

		# Check if username already exists
		existing_user = User.query.filter_by(username=username).first()
		if existing_user:
			response = {
				'error': 'Username already exists'
			}
			response_data = marshal(
				response,
				bad_request_model
			)
			return response_data, 400

		# Create new user
		new_user = User(
			username=username,
			password=password,  # In a real app, use proper password hashing
			client_id=client_id
		)

		# Save user to database
		db.session.add(new_user)
		db.session.commit()

		# Create access token
		access_token = create_access_token(identity=str(new_user.id))
		decoded_token = decode_token(access_token)
		issued_at = decoded_token['iat']
		expires_at = decoded_token['exp']

		# Create response
		response = {
			'user': {
				'id': new_user.id,
				'username': new_user.username,
				'client_id': new_user.client_id
			},
			'message': 'Registration successful',
			'access_token': access_token,
			'issued_at': issued_at,
			'expires_at': expires_at
		}

		response_data = marshal(
			response,
			post_auth_register_response_model
		)

		return response_data, 201


@auth_namespace.route('/me')
class AuthMeResource(Resource):
	@auth_namespace.doc(
		description=get_auth_me_description,
		order=3
	)
	@auth_namespace.response(
		code=200,
		model=get_auth_me_response_model,
		description="User data found"
	)
	@auth_namespace.response(
		code=401,
		model=not_authenticated_model,
		description="Not authenticated"
	)
	@authentication_required(not_authenticated_model)
	def get(self):
		# Get the current JWT
		jwt_data = get_jwt()

		# Get user from JWT
		user = get_user_from_jwt(jwt=jwt_data)

		# Get token timestamps
		issued_at = jwt_data.get('iat')
		expires_at = jwt_data.get('exp')

		# Create response
		response = {
			'user': {
				'id': user.id,
				'username': user.username,
				'client_id': user.client_id
			},
			'issued_at': issued_at,
			'expires_at': expires_at
		}

		response_data = marshal(
			response,
			get_auth_me_response_model
		)

		return response_data, 200
