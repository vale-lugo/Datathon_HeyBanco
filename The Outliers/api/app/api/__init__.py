from flask import Blueprint
from flask_restx import Api
from flask_jwt_extended import JWTManager

from app.api.routes import register_blueprints
from app.api.routes import register_namespaces


def register_routes(app):
	# Initialize JWT
	jwt = JWTManager(app)

	# Add user_lookup_loader callback
	@jwt.user_lookup_loader
	def user_lookup_callback(_jwt_header, jwt_data):
		from app.models import User
		identity = jwt_data["sub"]
		return User.query.filter_by(id=identity).one_or_none()

	# Set up API routes
	prefix = '/api'
	base_blueprint = Blueprint(
		name='base',
		import_name=__name__,
		url_prefix=prefix
	)
	rest_api = Api(
		app,
		version='1.0',
		title='API Documentation',
		description='API Documentation',
		doc='/docs',
		prefix=prefix
	)

	register_blueprints(base_blueprint)
	register_namespaces(rest_api)

	app.register_blueprint(base_blueprint)
