import os

import streamlit as st
from PIL import Image

from opciones.principal import show_principal
from opciones.productos import show_productos
from api_utils import login, logout, get_user_info, register

st.set_page_config(
	page_title="Hey Banco",
	layout="wide",
	initial_sidebar_state="collapsed"
)

with open('./estilo_fondo.css') as f:
	css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if 'submit' not in st.session_state:
	st.session_state['submit'] = False

if 'vista_actual' not in st.session_state:
	st.session_state['vista_actual'] = "inicio_sesion"


if 'username' not in st.session_state:
	st.session_state['username'] = None

if 'regresar' not in st.session_state:
	st.session_state['regresar'] = False


# file_path = 'vid_reports.xlsx'
# sheet_name = 'Result 1'
# df = pd.read_excel(file_path, sheet_name=sheet_name)

def cambiar_vista(nueva):
	st.session_state['vista_actual'] = nueva


def submit():
	st.session_state['submit'] = True


def regresar():
	st.session_state['submit'] = True


def on_change(key):
	seleccionado = st.session_state[key]
	st.session_state['seleccionado'] = seleccionado


def main():
	if st.session_state['vista_actual'] == "inicio_sesion":
		st.header("Inicia Sesión")

		with st.form("login_form"):
			usuario = st.text_input(label="Usuario", placeholder="Ingresa tu usuario", label_visibility="collapsed")
			contrasena = st.text_input(label="Contraseña", placeholder="Ingresa tu contraseña", type="password", label_visibility="collapsed")

			submit_button = st.form_submit_button("Iniciar Sesión")

			if submit_button:
				if not usuario:
					st.warning("Por favor ingresa tu usuario.")
				elif not contrasena:
					st.warning("Por favor ingresa tu contraseña.")
				else:
					# Authenticate with the API
					st.session_state['username'] = usuario
					st.session_state['password'] = contrasena
					success, error = login(usuario, contrasena)
					if success:
						cambiar_vista('principal')
						st.rerun()
					else:
						st.error(f"Error de autenticación: {error}")

		# Add a link to the registration form
		st.markdown("¿No tienes una cuenta? [Regístrate aquí](#)")
		if st.button("Crear cuenta nueva"):
			cambiar_vista('registro')
			st.rerun()

		# Mostrar imágenes
		try:
			img1 = Image.open(os.path.join("imagenes", "IMG_8632.PNG"))
			img2 = Image.open(os.path.join("imagenes", "IMG_8633.PNG"))
			img3 = Image.open(os.path.join("imagenes", "IMG_8634.PNG"))
			img4 = Image.open(os.path.join("imagenes", "IMG_8635.PNG"))

			col1, col2, col3 = st.columns(3)
			with col1:
				st.image(img1, use_container_width=True)
				st.image(img4, use_container_width=True)

			with col2:
				st.image(img2, use_container_width=True)

			with col3:
				st.image(img3, use_container_width=True)

		except FileNotFoundError as e:
			st.error(f"No se pudo cargar una imagen: {e.filename}")

	elif st.session_state['vista_actual'] == "registro":
		st.header("Registro de Usuario")

		with st.form("register_form"):
			usuario = st.text_input(label="Usuario", placeholder="Ingresa tu usuario", label_visibility="collapsed")
			contrasena = st.text_input(label="Contraseña", placeholder="Ingresa tu contraseña", type="password", label_visibility="collapsed")
			client_id = st.text_input(label="ID de Cliente", placeholder="Ingresa tu ID de cliente", label_visibility="collapsed")

			submit_button = st.form_submit_button("Registrarse")

			if submit_button:
				if not usuario:
					st.warning("Por favor ingresa tu usuario.")
				elif not contrasena:
					st.warning("Por favor ingresa tu contraseña.")
				elif not client_id:
					st.warning("Por favor ingresa tu ID de cliente.")
				else:
					# Register with the API
					success, error = register(usuario, contrasena, client_id)
					if success:
						st.success("Registro exitoso. Ahora puedes iniciar sesión.")
						# Redirect to login after a successful registration
						cambiar_vista('inicio_sesion')
						st.rerun()
					else:
						st.error(f"Error de registro: {error}")

		# Add a link back to the login form
		if st.button("Volver a Iniciar Sesión"):
			cambiar_vista('inicio_sesion')
			st.rerun()

		# Mostrar imágenes
		try:
			img1 = Image.open(os.path.join("imagenes", "IMG_8632.PNG"))
			img2 = Image.open(os.path.join("imagenes", "IMG_8633.PNG"))
			img3 = Image.open(os.path.join("imagenes", "IMG_8634.PNG"))
			img4 = Image.open(os.path.join("imagenes", "IMG_8635.PNG"))

			col1, col2, col3 = st.columns(3)
			with col1:
				st.image(img1, use_container_width=True)
				st.image(img4, use_container_width=True)

			with col2:
				st.image(img2, use_container_width=True)

			with col3:
				st.image(img3, use_container_width=True)

		except FileNotFoundError as e:
			st.error(f"No se pudo cargar una imagen: {e.filename}")

	elif st.session_state['vista_actual'] == "principal":
		show_principal()

	elif st.session_state['vista_actual'] == "productos":
		show_productos()
		if st.button('Volver a Principal', key="volver_productos_btn"):
			cambiar_vista('principal')
			st.rerun()


if __name__ == "__main__":
	main()
