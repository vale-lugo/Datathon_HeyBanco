from app.api.routes.client_data.resources import client_data_namespace


def register_client_data_namespace(rest_api):
	rest_api.add_namespace(client_data_namespace)