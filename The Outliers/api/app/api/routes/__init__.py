from app.api.routes.authentication import register_auth_namespace
from app.api.routes.client_data import register_client_data_namespace
from app.api.routes.transaction_data import register_transaction_data_namespace
from app.api.routes.predictions import register_predictions_routes
from app.api.routes.predictions.routes import register_predictions_namespace


def register_blueprints(base_blueprint):
	pass


def register_namespaces(rest_api):
	register_auth_namespace(rest_api)
	register_client_data_namespace(rest_api)
	register_transaction_data_namespace(rest_api)
	register_predictions_namespace(rest_api)
