from app.api.routes.authentication.resources import auth_namespace


def register_auth_namespace(rest_api):
	rest_api.add_namespace(auth_namespace)
