from flask import Blueprint
from flask_restx import Namespace
from flask_restx import fields

__all__ = [
    'predictions_namespace',
    'get_prediction_description',
    'get_prediction_response_model',
    'bad_request_model',
    'resource_not_found_model',
    'unauthorized_model',
    'not_authenticated_model'
]

# Create predictions blueprint
predictions_blueprint = Blueprint(
    name='predictions',
    import_name=__name__
)

# Create predictions namespace
predictions_namespace = Namespace(
    name='Predictions',
    description='Prediction operations',
    path='/predictions'
)

# Define request descriptions
get_prediction_description = (
    'Get current month\'s spending prediction for the authenticated user.'
    'Requires authentication.'
)

# Define prediction response model
get_prediction_response_model = predictions_namespace.model(
    name='PredictionResponse',
    model={
        'client_id': fields.String(
            description='Client ID',
            example='client123'
        ),
        'current_month_spend': fields.Float(
            description='Predicted spending for current month',
            example=1500.75
        )
    }
)

# Define error models
bad_request_model = predictions_namespace.model(
    name='BadRequest',
    model={
        'error': fields.String(
            description='Error message',
            example='Bad request'
        )
    }
)

resource_not_found_model = predictions_namespace.model(
    name='ResourceNotFound',
    model={
        'error': fields.String(
            description='Error message',
            example='Resource not found'
        )
    }
)

unauthorized_model = predictions_namespace.model(
    name='Unauthorized',
    model={
        'error': fields.String(
            description='Error message',
            example='Unauthorized'
        )
    }
)

not_authenticated_model = predictions_namespace.model(
    name='NotAuthenticated',
    model={
        'error': fields.String(
            description='Error message',
            example='Not authenticated'
        )
    }
)
