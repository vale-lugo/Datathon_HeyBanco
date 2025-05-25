import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
from datetime import datetime
from PIL import Image
import xgboost as xgb

# ---------------- FUNCIÓN PARA CONSTRUIR EL VECTOR ------------------

def construir_vector(user_id, fecha_prediccion):
    df = pd.read_csv("hey_df_1.csv", parse_dates=['fecha', 'fecha_nacimiento', 'fecha_alta'])
    fecha_prediccion = fecha_prediccion.replace(hour=0, minute=0, second=0, microsecond=0)

    historial = df[df['id'] == user_id].copy()
    historial = historial[historial['fecha'] < fecha_prediccion]

    if historial.empty:
        return None

    le_giro = LabelEncoder()
    le_actividad = LabelEncoder()
    le_giro.fit(df['giro_comercio'].astype(str))
    le_actividad.fit(df['actividad_empresarial'].astype(str))

    cliente = historial.sort_values('fecha').iloc[-1]

    id_estado = cliente['id_estado']
    actividad_empresarial = cliente['actividad_empresarial']
    giro_predicho = cliente['giro_comercio']
    edad = (fecha_prediccion - cliente['fecha_nacimiento']).days // 365
    antiguedad_cliente = (fecha_prediccion - cliente['fecha_alta']).days
    mes = fecha_prediccion.month
    dia_semana = fecha_prediccion.weekday()
    es_fin_de_semana = int(dia_semana in [5, 6])
    dias_desde_ultimo_gasto = (fecha_prediccion - cliente['fecha']).days

    try:
        monto_promedio_giro = historial[historial['giro_comercio'] == giro_predicho]['monto_promedio_giro'].iloc[-1]
    except IndexError:
        monto_promedio_giro = 0

    try:
        conteo_gastos_giro = historial[historial['giro_comercio'] == giro_predicho]['conteo_gastos_giro'].iloc[-1]
    except IndexError:
        conteo_gastos_giro = 0

    actividad_empresarial_encoded = le_actividad.transform([str(actividad_empresarial)])[0]
    giro_comercio_encoded = le_giro.transform([str(giro_predicho)])[0]

    tipo_persona_dummy = cliente.get('tipo_persona_Persona Fisica Sin Actividad Empresarial', 0)
    genero_F = cliente.get('genero_F', 0)
    genero_M = cliente.get('genero_M', 0)
    tipo_venta_fisica = cliente.get('tipo_venta_fisica', 0)

    vector = [
        id_estado,
        actividad_empresarial_encoded,
        giro_comercio_encoded,
        edad,
        antiguedad_cliente,
        mes,
        dia_semana,
        es_fin_de_semana,
        tipo_persona_dummy,
        genero_F,
        genero_M,
        tipo_venta_fisica,
        monto_promedio_giro,
        conteo_gastos_giro,
        dias_desde_ultimo_gasto
    ]

    return np.array(vector).reshape(1, -1)

# ----------------- CARGA DE MODELOS -----------------------

amount = joblib.load("C:/Users/Paco Llanas/Downloads/xgb_modelo_monto_pkl.pkl")['modelo']
recurrency = joblib.load("C:/Users/Paco Llanas/Downloads/model_classifier.pkl")
days_dict = joblib.load("C:/Users/Paco Llanas/Downloads/xbg_modelo_dias_pkl.pkl")
days = days_dict['modelo']

# ------------------------ STREAMLIT UI ---------------------

def main():
    st.set_page_config(page_title="Predict App", layout="wide")

    with st.sidebar:
        st.title("Bienvenido a Hey Banco")
        st.markdown("""
        <style>
            .container {
                width: 100%;
                margin: 0 auto;
                padding: 20px;
            }
            .app-title {
                font-size: 2.5rem;
                color: #000000;
                text-align: center;
                margin-bottom: 20px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            input, select, textarea {
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        body {
            background-color: #FCFCF5;
        }

        .stApp {
            background-color: #FCFCF5;
        }

        header, footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
        <style>
        /* Cambiar el color del texto activo de las tabs */
        .stTabs [data-baseweb="tab"] {
            color: gray;
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
        }

        /* Cambiar el color del tab activo */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #000000 !important; /* color de fondo activo */
            color: white !important;             /* color del texto activo */
            font-weight: bold; border-bottom: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        "App",
        "Plan de acción",
        "Variables de interés",
    ])

    # ----------- TAB: APP -----------------
    with tabs[0]:
        st.image("C:/Users/Paco Llanas/Downloads/hey.png", use_container_width=True)
        st.markdown(
            "<h1 style='text-align: center; color: #000000;'>App de Predicción de Hey Banco</h1>",
            unsafe_allow_html=True
        )

        col1 = st.columns(1)[0]

        with col1:
            st.markdown(
                """
                <h3 style='text-align: center; color: #000000; font-family: Roboto, monospace;'>
                    Identificación de Usuario
                </h3>
                """,
                unsafe_allow_html=True
            )
            user_id_input = st.text_input(" ", placeholder="Ingresa tu ID de usuario", key="user_id_input")

            if user_id_input:
                try:
                    user_id = int(user_id_input)
                    fecha = st.date_input("Fecha de predicción", value=datetime.today()).strftime("%Y-%m-%d")
                    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")

                    st.markdown("---")
                    st.markdown("<h4 style='color:#004080;'>Zona de predicción personalizada:</h4>", unsafe_allow_html=True)

                    vector = construir_vector(user_id, fecha_dt)

                    if vector is not None:
                        dvector = xgb.DMatrix(vector)
                        pred_monto = amount.predict(dvector)[0]
                        pred_rec = recurrency.predict(vector)[0]
                        pred_dias = days.predict(dvector)[0]

                        st.markdown(
                            f"<span style='color: green; font-weight: bold;'>💰 Monto estimado del próximo gasto: ${pred_monto:.2f}</span>",
                            unsafe_allow_html=True
                        )

                        # Mensaje 2 - Cliente recurrente
                        st.markdown(
                            f"<span style='color: blue; font-weight: bold;'>🔁 ¿Es cliente recurrente?: {'Sí' if pred_rec == 1 else 'No'}</span>",
                            unsafe_allow_html=True
                        )

                        # Mensaje 3 - Días hasta siguiente gasto
                        st.markdown(
                            f"<span style='color: orange; font-weight: bold;'>📅 Días estimados hasta el siguiente gasto: {int(pred_dias)} días</span>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.error("No se encontró historial suficiente para este usuario antes de la fecha dada.")

                except ValueError:
                    st.error("Por favor ingresa un número de ID válido.")

    # ----------- OTRAS TABS -----------------
    with tabs[1]:
        st.markdown('<h2 style="color:black;">Plan de acción</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:black;">Nuestro objetivo en este proyecto es desarrollar un modelo predictivo capaz de identificar y anticipar los gastos recurrentes de los clientes. Esta predicción no solo considera la probabilidad de que un gasto se repita, sino que también busca estimar cuándo ocurrirá, cuánto se gastará.</p>', unsafe_allow_html=True)
    with tabs[2]:
        st.markdown('<h2 style="color:black;">Variables de interés</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:black;">Variables del tipo predictoras.</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
