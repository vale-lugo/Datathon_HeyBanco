import streamlit as st
from api_utils import get_user_info, logout

def show_productos():
    # Get user info from API
    user_info, error = get_user_info()
    if error:
        st.error(f"Error al obtener información del usuario: {error}")
        return

    # Display user info
    username = user_info.get('user', {}).get('username', 'Usuario')

    # Add sidebar for navigation
    with st.sidebar:
        st.title(f"Hey, {username}")
        st.markdown("### Navegación")

        # Navigation options with improved styling
        st.markdown("""
        <style>
        div.stButton > button {
            width: 100%;
            background-color: #2c2c2c;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px;
            margin-bottom: 10px;
            text-align: left;
        }
        div.stButton > button:hover {
            background-color: #444;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("Inicio", key="inicio_btn"):
            st.session_state['vista_actual'] = "principal"
            st.rerun()

        if st.button("Análisis de gastos", key="analisis_btn"):
            st.session_state['vista_actual'] = "principal"
            st.session_state['scroll_to_analysis'] = True
            st.rerun()

        if st.button("Productos disponibles", key="productos_btn"):
            st.session_state['vista_actual'] = "productos"
            st.rerun()

        # Add Hey Coins and Referidos as visual components
        st.markdown("### Mis Beneficios")

        # Hey Coins visual component
        st.markdown("""
        <div style="background-color: #2c2c2c; border-radius: 10px; padding: 15px; display: flex; justify-content: 
        space-between; align-items: center; margin-bottom: 10px;">
            <div style="display: flex; align-items: center;">
                <div style="background-color: #0d7f1b; padding: 8px; border-radius: 6px; margin-right: 8px;">
                    🪙
                </div>
                <div style="color: white; font-weight: bold; font-size: 14px;">Hey Coins</div>
            </div>
            <div style="text-align: right; color: white;">
                <div style="font-weight: bold; font-size: 14px;">0</div>
                <div style="font-size: 12px; color: #ccc;">Total Hey Coins</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Referidos visual component
        st.markdown("""
        <div style="background-color: #2c2c2c; border-radius: 10px; padding: 15px; display: flex; justify-content: 
        space-between; align-items: center; margin-bottom: 10px;">
            <div style="display: flex; align-items: center;">
                <div style="background-color: #7f690d; padding: 8px; border-radius: 6px; margin-right: 8px;">
                    👥
                </div>
                <div style="color: white; font-weight: bold; font-size: 14px;">Referidos</div>
            </div>
            <div style="text-align: right; color: white;">
                <div style="font-weight: bold; font-size: 14px;">0</div>
                <div style="font-size: 12px; color: #ccc;">Mis referidos</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Cuenta")
        if st.button("Cerrar sesión", key="logout_btn"):
            logout()
            st.session_state['vista_actual'] = "inicio_sesion"
            st.rerun()

    # Main content
    st.title("Productos disponibles para tí")

    # Combine all products into a single list for auto-scrolling
    all_products = [
        ("Tarjeta de Crédito", "¡Obtén MSI, recompensas y más!"),
        ("Tarjeta de Crédito con Garantía*", "La mejor opción para aprender a usar una tajeta de crédito"),
        ("Crédito personal", "Solicita desde $1,000 hasta $4,000"),
        ("Crédito de auto", "¡Encuentra tu auto al precio que quieres!"),
        ("Cuenta para menores", "Enséñale a tus hijos a manejar su dinero"),
        ("Ahorro", "Mantén hasta 5 ahorros activos al mismo tiempo"),
        ("Ahorro Inmediato", "Ahorra un % por cada gasto que hagas")
    ]

    # Add CSS for improved auto-scrolling carousel
    st.markdown("""
    <style>
    .product-carousel {
        overflow: hidden;
        position: relative;
        height: 300px;
        margin-bottom: 20px;
    }
    .product-container {
        animation: scrollProducts 30s linear infinite;
        position: absolute;
        width: 100%;
    }
    .product-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        width: 100%;
    }
    .product-card {
        background-color: #2c2c2c;
        border-radius: 10px;
        padding: 15px;
        width: 48%;
        box-sizing: border-box;
    }
    .product-title {
        color: white;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .product-description {
        color: #ccc;
        font-size: 12px;
    }
    @keyframes scrollProducts {
        0% { transform: translateY(0); }
        100% { transform: translateY(-100%); }
    }
    </style>

    <div class="product-carousel">
        <div class="product-container">
    """, unsafe_allow_html=True)

    # Create product rows (2 products per row)
    for i in range(0, len(all_products), 2):
        st.markdown('<div class="product-row">', unsafe_allow_html=True)

        # First product in row
        product, description = all_products[i]
        st.markdown(f"""
        <div class="product-card">
            <div class="product-title">{product}</div>
            <div class="product-description">{description}</div>
        </div>
        """, unsafe_allow_html=True)

        # Second product in row (if exists)
        if i + 1 < len(all_products):
            product, description = all_products[i + 1]
            st.markdown(f"""
            <div class="product-card">
                <div class="product-title">{product}</div>
                <div class="product-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Empty card if odd number of products
            st.markdown('<div class="product-card"></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Duplicate the products for continuous scrolling
    for i in range(0, len(all_products), 2):
        st.markdown('<div class="product-row">', unsafe_allow_html=True)

        # First product in row
        product, description = all_products[i]
        st.markdown(f"""
        <div class="product-card">
            <div class="product-title">{product}</div>
            <div class="product-description">{description}</div>
        </div>
        """, unsafe_allow_html=True)

        # Second product in row (if exists)
        if i + 1 < len(all_products):
            product, description = all_products[i + 1]
            st.markdown(f"""
            <div class="product-card">
                <div class="product-title">{product}</div>
                <div class="product-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Empty card if odd number of products
            st.markdown('<div class="product-card"></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Close the carousel container
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
