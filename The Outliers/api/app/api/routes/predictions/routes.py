from app.api.routes.predictions.resources import predictions_namespace

def register_predictions_routes():
    # This function is intentionally left empty as the namespace is registered
    # in the register_predictions_namespace function in app/api/routes/__init__.py
    pass

def register_predictions_namespace(rest_api):
    # Register the main namespace
    rest_api.add_namespace(predictions_namespace)