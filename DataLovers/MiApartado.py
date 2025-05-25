import streamlit as st

st.set_page_config(page_title="Mi Apartado", layout="centered")

# Estilos CSS para tarjetas y botón
st.markdown("""
    <style>
        .card {
            background-color: #1e1e1e;
            border-radius: 12px;
            padding: 15px 20px;
            margin-bottom: 15px;
            color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.6);
        }
        .card-title {
            font-weight: 700;
            font-size: 18px;
            margin-bottom: 8px;
        }
        .card-text {
            font-size: 16px;
            margin-bottom: 4px;
        }
        .btn-back {
            background-color: #2288ff;
            border: none;
            color: white;
            padding: 10px 18px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s ease;
            margin-top: 20px;
            width: 100%;
        }
        .btn-back:hover {
            background-color: #1766cc;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Pagos Recurrentes")

st.subheader("Tus pagos mensuales")
pagos = [
    {"nombre": "Spotify", "monto": 129},
    {"nombre": "Netflix", "monto": 229},
    {"nombre": "Telcel", "monto": 399},
    {"nombre": "Gimnasio", "monto": 450},
]

for pago in pagos:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">{pago['nombre']}</div>
        <div class="card-text">${pago['monto']:.2f} MXN</div>
    </div>
    """, unsafe_allow_html=True)

st.subheader("Descuentos sugeridos por tus pagos")
descuentos = [
    "10% de cashback en tiendas digitales si pagas Spotify y Netflix",
    "$50 de descuento en tu recibo Telcel si domicilias el pago",
    "Promoción: 2x1 en membresía de gimnasio si pagas con Hey Card"
]

for desc in descuentos:
    st.markdown(f"""
    <div class="card" style="background-color: #2a2a2a;">
        <div class="card-text">- {desc}</div>
    </div>
    """, unsafe_allow_html=True)

# Botón para regresar con estilo personalizado

