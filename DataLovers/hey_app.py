import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hey App - Simulación", layout="centered")

# ---- Estado inicial ----
if "show_payment_notice" not in st.session_state:
    st.session_state.show_payment_notice = True

if "balance" not in st.session_state:
    st.session_state.balance = 2500.0

# ---- Estilos CSS personalizados ----
st.markdown("""
    <style>
        body {
            background-color: #111;
        }
        .card {
            background-color: #1e1e1e;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 1rem;
            color: white;
        }
        .blue-banner {
            background-color: #2288ff;
            padding: 0.75rem;
            border-radius: 0.5rem;
            color: white;
            font-weight: bold;
            text-align: center;
        }
        .section-title {
            font-weight: bold;
            font-size: 1.1rem;
            color: #ffffffdd;
            margin-top: 1rem;
        }
        .product-card {
            background-color: #2a2a2a;
            padding: 0.75rem;
            border-radius: 0.75rem;
            margin-bottom: 0.5rem;
            color: white;
        }
        .balance {
            color: #ccc;
            font-size: 0.9rem;
        }
        .nav-bar {
            background-color: #1e1e1e;
            padding: 0.75rem;
            display: flex;
            justify-content: space-around;
            border-top: 1px solid #333;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        .nav-item {
            color: #bbb;
            text-align: center;
            font-size: 0.8rem;
        }
        .notice-card {
            background-color: #323232;
            padding: 1rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            color: white;
        }
        .button-container {
            display: flex;
            gap: 1rem;
            margin-top: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Contenido principal ----
st.title("Bienvenido a Hey App")

# Imagen superior
st.image("https://cashback.visa.com.mx/inc/images/bancos_logos/hey.png", use_container_width=True)

# Notificación emergente (visible siempre hasta ignorar/pagar)
if st.session_state.show_payment_notice:
    st.markdown("""
    <div class="notice-card">
        🔔 <strong>Tienes un pago pronto</strong><br>
        Cerca de esta fecha realizas un pago a <strong>'Gaby M'</strong>.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ignorar"):
            st.session_state.show_payment_notice = False
    with col2:
        if st.button("Pagar"):
            if st.session_state.balance >= 200:
                st.session_state.balance -= 200
                st.success("Pago realizado con éxito.")
            else:
                st.warning("Saldo insuficiente para realizar el pago.")
            st.session_state.show_payment_notice = False

# Productos contratados
st.markdown("<div class='section-title'>Mis productos contratados</div>", unsafe_allow_html=True)
st.markdown(f"""
<div class="card">
    <strong>Cuentas</strong><br>
    <span class="balance">${st.session_state.balance:,.2f}</span>
    <hr>
    <strong>Hey Coins</strong><br>
    <span class="balance">0</span>
    <hr>
    <strong>Refiere a tus amigos</strong><br>
    <span class="balance">0</span>
</div>
""", unsafe_allow_html=True)

# Productos disponibles
st.markdown("<div class='section-title'>Productos disponibles para ti</div>", unsafe_allow_html=True)
# --- Botón simulado para Mi Apartado ---
if "go_to_apartado" not in st.session_state:
    st.session_state.go_to_apartado = False

col1, col2 = st.columns([1, 6])
with col1:
    if st.button("🟡", key="apartado_btn"):
        st.session_state.go_to_apartado = True
with col2:
    st.markdown("""
    <div class="product-card-btn">
        <b>Mi Apartado</b><br>
        <small>Consulta tus gastos próximos y descuentos</small>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.go_to_apartado:
    st.session_state.go_to_apartado = False  # reset
    st.switch_page("pages/MiApartado.py")

st.markdown("""
<div class="product-card">💳 Tarjeta de Crédito con Garantía<br><small>La mejor opción para aprender a usar una tarjeta</small></div>
<div class="product-card">💰 Crédito personal<br><small>Solicita desde $1,000 hasta $400,000</small></div>
<div class="product-card">🚗 Crédito de auto<br><small>¡Encuentra tu auto al precio que quieres!</small></div>
""", unsafe_allow_html=True)

# Barra de navegación inferior
st.markdown("""
<div class="nav-bar">
    <div class="nav-item">🏠<br>Inicio</div>
    <div class="nav-item">💳<br>Pagos</div>
    <div class="nav-item">🌀<br>Hey</div>
    <div class="nav-item">📩<br>Buzón</div>
</div>
""", unsafe_allow_html=True)
