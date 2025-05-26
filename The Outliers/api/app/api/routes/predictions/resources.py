from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    current_user
)
from flask_restx import (
    Resource,
    marshal
)
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import os

from app.api.routes.predictions.models import *
from app.models import TransactionData, ClientData
from app.utils.validations import authentication_required

# Load the model
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), 
                         'model_service', 'models', 'lightgbm_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Define feature columns used by the model - matching modelo_marco.ipynb
feature_cols = [
    'month_num', 'year', 'monto_prev', 'rolling_3', 'id', 
    'id_municipio', 'id_estado', 'tipo_persona', 'genero', 'actividad_empresarial'
]

# Define categorical features
cat_features = ['id', 'tipo_persona', 'genero', 'actividad_empresarial']

@predictions_namespace.route('')
class PredictionResource(Resource):
    @predictions_namespace.doc(
        description=get_prediction_description
    )
    @predictions_namespace.response(
        code=200,
        model=get_prediction_response_model,
        description="Prediction successful"
    )
    @predictions_namespace.response(
        code=401,
        model=not_authenticated_model,
        description="Not authenticated"
    )
    @predictions_namespace.response(
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

        # Get transaction data for the client
        transactions = TransactionData.query.filter_by(client_id=client_data.id).all()

        if not transactions:
            response = {
                'error': 'No transaction data found for this client'
            }
            response_data = marshal(
                response,
                resource_not_found_model
            )
            return response_data, 404

        # Prepare data for prediction
        try:
            # Convert transactions to DataFrame
            txn_data = []
            for t in transactions:
                txn_data.append({
                    'id': client_data.id,
                    'fecha': t.fecha,
                    'monto': t.monto,
                    'comercio': t.comercio,
                    'giro_comercio': t.giro_comercio,
                    'tipo_venta': t.tipo_venta
                })

            txn_df = pd.DataFrame(txn_data)

            # Process transaction data - matching modelo_marco.ipynb approach
            txn_df["fecha"] = pd.to_datetime(txn_df["fecha"])
            txn_df["month"] = txn_df["fecha"].dt.to_period("M")

            # Step 1: Aggregate monthly expense per client
            monthly_expenses = txn_df.groupby(["id", "month"])["monto"].sum().reset_index()
            monthly_expenses.rename(columns={"monto": "monto_total"}, inplace=True)
            monthly_expenses["month"] = monthly_expenses["month"].dt.to_timestamp()

            # Step 2: Add client features
            # Create a DataFrame from the client data dictionary
            client_df = pd.DataFrame([{
                "id": client_data.id,
                "fecha_nacimiento": client_data.fecha_nacimiento,
                "fecha_alta": client_data.fecha_alta,
                "id_municipio": client_data.id_municipio,
                "id_estado": client_data.id_estado,
                "tipo_persona": client_data.tipo_persona,
                "genero": client_data.genero,
                "actividad_empresarial": client_data.actividad_empresarial
            }])

            # Merge with monthly expenses
            df = monthly_expenses.merge(
                client_df,
                on="id", 
                how="left"
            )

            # Temporal features
            df["month_num"] = df["month"].dt.month
            df["year"] = df["month"].dt.year

            # Sort for rolling calculations
            df = df.sort_values(["id", "month"])

            # Lag & rolling features
            df["monto_prev"] = df.groupby("id")["monto_total"].shift(1)
            df["rolling_3"] = df.groupby("id")["monto_total"].rolling(3).mean().reset_index(0, drop=True)

            # Drop NaNs from rolling/lags
            df = df.dropna(subset=["monto_prev", "rolling_3"])

            # Ensure categorical features are category type
            for col in cat_features:
                df[col] = df[col].astype("category")

            # Make prediction - matching modelo_marco.ipynb approach
            if len(df) < 3:  # Need at least some history for prediction
                # Not enough history, use a default value
                prediction = 0
            else:
                # Get the most recent month's data
                features = df.sort_values("month").tail(1)

                # Make prediction - predicting monto_total (current month's spending)
                prediction = float(model.predict(features[feature_cols]))

            # Create response
            response = {
                'client_id': client_data.id,
                'current_month_spend': prediction  # Model predicts current month's spending (monto_total)
            }

            response_data = marshal(
                response,
                get_prediction_response_model
            )

            return response_data, 200

        except Exception as e:
            response = {
                'error': f'Error making prediction: {str(e)}'
            }
            response_data = marshal(
                response,
                bad_request_model
            )
            return response_data, 400
