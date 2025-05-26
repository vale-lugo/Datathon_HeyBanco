import streamlit as st
import pandas as pd
from collections import defaultdict
from datetime import datetime
import plotly.express as px
from api_utils import get_user_info, get_client_data, get_transactions, get_category_spending, get_statistics, get_monthly_report, get_predictions




def show_principal():

	# Get user info from API
	user_info, error = get_user_info()
	if error:
		st.error(f"Error al obtener información del usuario: {error}")
		return

	# Get client data from API
	client_data, error = get_client_data()
	if error:
		st.error(f"Error al obtener datos del cliente: {error}")
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
			from api_utils import logout
			logout()
			st.session_state['vista_actual'] = "inicio_sesion"
			st.rerun()

	# Main content
	st.title("Dashboard Principal")

	# Add action buttons at the top
	st.markdown("""
	<div style="display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap;">
		<div style="background-color: #e0e0ff; padding: 8px 16px; border-radius: 15px; color: 
		#2c2c2c; font-size: 14px; font-weight: bold; text-align: center; cursor: pointer;">Tarjetas</div>
		<div style="background-color: #e0e0ff; padding: 8px 16px; border-radius: 15px; color: 
		#2c2c2c; font-size: 14px; font-weight: bold; text-align: center; cursor: pointer;">Movimientos</div>
		<div style="background-color: #e0e0ff; padding: 8px 16px; border-radius: 15px; color: 
		#2c2c2c; font-size: 14px; font-weight: bold; text-align: center; cursor: pointer;">Transferir</div>
	</div>
	""", unsafe_allow_html=True)

	st.markdown("""<div style="text-align: left;"> <h4>Mis productos contratados</h4></div>""", unsafe_allow_html=True)

	# Create two columns for Cuentas and Cuenta Hey components
	col_accounts1, col_accounts2 = st.columns(2)

	with col_accounts1:
		# Cuentas component
		st.markdown(""" 
		<div style="background-color: #2c2c2c; border-radius: 10px; padding: 15px; display: flex; justify-content: 
		space-between; align-items: center; height: 120px;">
			<div style="display: flex; align-items: center;">
				<div style="background-color: #b29efc; padding: 8px; border-radius: 6px; margin-right: 8px;">
					💲
				</div>
				<div style="color: white; font-weight: bold; font-size: 16px;">Cuentas</div>
			</div>
			<div style="text-align: right; color: white;">
				<div style="font-weight: bold; font-size: 16px;">$0.00</div>
				<div style="font-size: 12px; color: #ccc;">Suma total de las cuentas</div>
			</div>
		</div>
		""", unsafe_allow_html=True)

	with col_accounts2:
		# Cuenta Hey component
		st.markdown("""
		<div style="background-color: #2c2c2c; padding: 15px; color: white; border-radius: 10px; display: 
		flex; justify-content: space-between; align-items: center; height: 120px;">
			<div>
				<div style="font-weight: bold; font-size: 16px;">Cuenta Hey *0011</div>
				<div><a href="#" style="color: #4da6ff; font-size: 12px;">Ver Cuenta y CLABE</a></div>
			</div>
			<div style="text-align: right;">
				<div style="font-weight: bold; font-size: 16px;">$0.00</div>
				<div style="font-size: 12px; color: #ccc;">Saldo disponible</div>
			</div>
		</div>
		""", unsafe_allow_html=True)

	# Define html_code for backward compatibility (in case it's used elsewhere)
	html_code = ""

	html_code_2 = """
    <div style="background-color: #2c2c2c; border-radius: 10px; padding: 20px; display: flex; justify-content: 
    space-between; align-items: center;">
        <div style="display: flex; align-items: center;">
            <div style="background-color: #0d7f1b; padding: 10px; border-radius: 8px; margin-right: 10px;">
                🪙
            </div>
            <div style="color: white; font-weight: bold; font-size: 18px;">Hey Coins</div>
        </div>
        <div style="text-align: right; color: white;">
            <div style="font-weight: bold; font-size: 18px;">0</div>
            <div style="font-size: 14px; color: #ccc;">Total Hey Coins</div>
        </div>
    </div>
    """

	html_code_3 = """
    <div style="background-color: #2c2c2c; border-radius: 10px; padding: 20px; display: flex; justify-content: 
    space-between; align-items: center;">
        <div style="display: flex; align-items: center;">
            <div style="background-color: #7f690d; padding: 10px; border-radius: 8px; margin-right: 10px;">
                👥
            </div>
            <div style="color: white; font-weight: bold; font-size: 18px;">Refiere a tus amigos</div>
        </div>
        <div style="text-align: right; color: white;">
            <div style="font-weight: bold; font-size: 18px;">0</div>
            <div style="font-size: 14px; color: #ccc;">Mis referidos</div>
        </div>
    </div>
    """

	st.markdown(html_code, unsafe_allow_html=True)


	# Transaction Analysis Section - Moved up to be just below accounts
	st.markdown("<hr>", unsafe_allow_html=True)

	# Análisis de gastos section
	st.markdown("""<div style="text-align: left;"> <h3>Análisis de gastos</h3></div>""", unsafe_allow_html=True)

	# Get statistics data from API
	statistics_data, error = get_statistics()
	if error:
		st.error(f"Error al obtener datos de estadísticas: {error}")
		return

	# Get transaction data from API (as fallback)
	transactions_data, error = get_transactions(per_page=100)  # Get up to 100 transactions
	if error:
		st.error(f"Error al obtener datos de transacciones: {error}")
		return

	# Extract transactions from response (for fallback)
	json_data = []
	for transaction in transactions_data.get('transactions', []):
		json_data.append({
			"fecha": transaction.get('fecha', ''),
			"monto": transaction.get('monto', 0),
			"giro_comercio": transaction.get('giro_comercio', 'Sin categoría'),
			"comercio": transaction.get('comercio', '')
		})

	# Diccionario para traducir meses de inglés a español
	mes_ingles_a_espanol = {
		"January": "Enero",
		"February": "Febrero",
		"March": "Marzo",
		"April": "Abril",
		"May": "Mayo",
		"June": "Junio",
		"July": "Julio",
		"August": "Agosto",
		"September": "Septiembre",
		"October": "Octubre",
		"November": "Noviembre",
		"December": "Diciembre"
	}

	# Process spending trends from statistics
	spending_trends = statistics_data.get('spending_trends', [])

	# Convert spending trends to the format we need
	gastos_ordenados = []
	for trend in spending_trends:
		period = trend.get('period', '')  # Format: YYYY-MM
		if period:
			year, month = period.split('-')
			month_name = datetime(int(year), int(month), 1).strftime("%B")
			month_year = f"{month_name} {year}"
			amount = trend.get('amount', 0)
			gastos_ordenados.append((month_year, amount))

	# If no spending trends, fallback to calculating from transactions
	if not gastos_ordenados:
		gastos_por_mes = defaultdict(float)
		for transaccion in json_data:
			fecha_str = transaccion["fecha"]
			monto = float(transaccion["monto"])
			try:
				# Try to parse ISO format (YYYY-MM-DDThh:mm:ss)
				fecha = datetime.fromisoformat(fecha_str.split('T')[0] if 'T' in fecha_str else fecha_str)
			except ValueError:
				try:
					# Fallback to MM/DD/YYYY format
					fecha = datetime.strptime(fecha_str, "%m/%d/%Y")
				except ValueError:
					# Skip this transaction if date can't be parsed
					continue
			clave_mes = fecha.strftime("%B %Y")  # Ej. "January 2025"
			gastos_por_mes[clave_mes] += monto

		# Ordenar por fecha (creamos tuplas con objeto datetime para ordenarlas)
		gastos_ordenados = sorted(gastos_por_mes.items(), key=lambda x: datetime.strptime(x[0], "%B %Y"))

	# Get all months from the API
	todos_los_meses = gastos_ordenados

	# Get current month data
	if gastos_ordenados:
		mes_actual = gastos_ordenados[-1][0]
		monto_actual = gastos_ordenados[-1][1]

		# Traducir mes actual a español
		mes_ingles, anio = mes_actual.split()
		mes_actual_es = f"{mes_ingles_a_espanol.get(mes_ingles, mes_ingles)} {anio}"

		# Get change percentage from statistics
		if len(spending_trends) >= 1:
			delta_actual = spending_trends[-1].get('change_percentage', 0)
			color = "red" if delta_actual >= 0 else "green"
		else:
			# Fallback to calculating manually
			if len(gastos_ordenados) >= 2:
				monto_anterior = gastos_ordenados[-2][1]
				delta_actual = ((monto_actual - monto_anterior) / monto_anterior) * 100
				color = "red" if delta_actual >= 0 else "green"
			else:
				delta_actual = 0
				color = "black"  # color por defecto en caso de no tener comparación
	else:
		mes_actual_es = "Sin datos"
		monto_actual = 0
		delta_actual = 0
		color = "black"

	# Mostrar gasto mensual y análisis de categorías
	col1, col2 = st.columns([1, 1])

	with col1:
		st.subheader(f"Gasto del mes {mes_actual_es}")

		html_monto_con_cambio = f"""
		<div style="text-align: left; line-height: 1.2;">
			<div style="font-size: 1.5em; font-weight: bold;">${monto_actual:,.2f}</div>
			<div style="color:{color}; font-size: 0.9em;">
				<b>{delta_actual:+.1f}% respecto</b><br>
				<small>al mes anterior</small>
			</div>
		</div>
		"""

		st.markdown(html_monto_con_cambio, unsafe_allow_html=True)

		# Crear tabla con porcentaje de cambio para todos los meses
		tabla_mensual = []

		# Map month names to their corresponding spending trend data
		month_to_trend = {}
		for trend in spending_trends:
			period = trend.get('period', '')  # Format: YYYY-MM
			if period:
				year, month = period.split('-')
				month_name = datetime(int(year), int(month), 1).strftime("%B")
				month_year = f"{month_name} {year}"
				month_to_trend[month_year] = trend

		for mes, monto in todos_los_meses:
			mes_ingles, anio = mes.split()
			mes_es = f"{mes_ingles_a_espanol.get(mes_ingles, mes_ingles)} {anio}"

			# Get change percentage from statistics if available
			if mes in month_to_trend and 'change_percentage' in month_to_trend[mes]:
				delta = month_to_trend[mes]['change_percentage']
				cambio = f"{delta:+.1f}%"
			else:
				# Fallback to the old method if statistics data is not available
				if len(tabla_mensual) == 0:
					cambio = "—"
				else:
					# Get the previous month's amount from the last entry in tabla_mensual
					prev_monto = float(tabla_mensual[-1]["Monto"].replace('$', '').replace(',', ''))
					if prev_monto > 0:
						delta = ((monto - prev_monto) / prev_monto) * 100
						cambio = f"{delta:+.1f}%"
					else:
						cambio = "—"

			tabla_mensual.append(
				{
					"Mes": mes_es,
					"Monto": f"${monto:,.2f}",
					"Cambio vs. mes anterior": cambio
				}
			)

		st.markdown("### Tabla de gasto mensual")
		# Convert to DataFrame and hide index to remove the index column
		df_tabla = pd.DataFrame(tabla_mensual)
		st.table(df_tabla.set_index('Mes'))

	with col2:
		st.markdown("### Tipo de comercio")

		# Get monthly report data from API
		monthly_data, error = get_monthly_report()

		if error:
			st.error(f"Error al obtener datos del reporte mensual: {error}")
		else:
			# Initialize session state for current month index if not exists
			if 'current_month_index' not in st.session_state:
				st.session_state['current_month_index'] = 0

			# Get monthly summaries from the data
			monthly_summaries = monthly_data.get('monthly_summaries', [])
			total_months = monthly_data.get('total_months', 0)

			if not monthly_summaries:
				st.warning("No hay datos de reportes mensuales disponibles.")
			else:
				# Create navigation buttons
				col_prev, col_month, col_next = st.columns([1, 2, 1])

				with col_prev:
					if st.button("← Anterior", key="prev_month", disabled=st.session_state['current_month_index'] >= len(monthly_summaries) - 1):
						st.session_state['current_month_index'] += 1
						st.rerun()

				with col_month:
					if monthly_summaries:
						current_month_data = monthly_summaries[st.session_state['current_month_index']]
						month_str = current_month_data.get('month', 'N/A')
						try:
							# Convert YYYY-MM to Month YYYY format
							year, month = month_str.split('-')
							month_name = datetime(int(year), int(month), 1).strftime("%B")
							formatted_month = f"{month_name} {year}"
						except:
							formatted_month = month_str

						st.markdown(f"<h4 style='text-align: center;'>{formatted_month}</h4>", unsafe_allow_html=True)

				with col_next:
					if st.button("Siguiente →", key="next_month", disabled=st.session_state['current_month_index'] <= 0):
						st.session_state['current_month_index'] -= 1
						st.rerun()

				# Display current month data
				if monthly_summaries:
					current_month_data = monthly_summaries[st.session_state['current_month_index']]

					# Display summary information using custom HTML/CSS for consistent sizing
					total_amount = current_month_data.get('total_amount', 0)
					transaction_count = current_month_data.get('transaction_count', 0)
					average_amount = current_month_data.get('average_amount', 0)

					# Create two columns with equal width
					col_amount, col_count = st.columns(2)

					# Custom HTML for Monto Total with fixed height
					with col_amount:
						st.markdown(f"""
						<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6; height: 120px; display: flex; flex-direction: column;">
							<p style="color: #31333F; margin-bottom: 0.2rem; font-size: 0.8rem; font-weight: 600;">Monto Total</p>
							<p style="color: #31333F; margin-bottom: 0; font-size: 1.5rem; font-weight: 600;">${"" if total_amount is None else f"{total_amount:,.2f}"}</p>
							<div style="flex-grow: 1;"></div>
						</div>
						""", unsafe_allow_html=True)

					# Custom HTML for Transacciones with Promedio and fixed height
					with col_count:
						st.markdown(f"""
						<div style="padding: 1rem; border-radius: 0.5rem; background-color: #f0f2f6; height: 120px; display: flex; flex-direction: column;">
							<p style="color: #31333F; margin-bottom: 0.2rem; font-size: 0.8rem; font-weight: 600;">Transacciones</p>
							<p style="color: #31333F; margin-bottom: 0; font-size: 1.5rem; font-weight: 600;">{"" if transaction_count is None else f"{transaction_count}"}</p>
							<div style="flex-grow: 1;"></div>
							<p style="color: #31333F; margin-bottom: 0; font-size: 0.8rem;">Promedio: ${"" if average_amount is None else f"{average_amount:,.2f}"}</p>
						</div>
						""", unsafe_allow_html=True)

					# Display top categories
					st.markdown("#### Top Categorías")
					top_categories = current_month_data.get('top_categories', [])

					if top_categories:
						# Create a DataFrame for better display
						categories_df = pd.DataFrame([
							{
								"Categoría": cat.get('category', 'Sin categoría'),
								"Monto": f"${cat.get('amount', 0):,.2f}",
								"Porcentaje": f"{cat.get('percentage', 0):,.2f}%"
							} for cat in top_categories
						])

						st.dataframe(categories_df, use_container_width=True, hide_index=True)

	# Add prediction section
	st.markdown("<hr>", unsafe_allow_html=True)
	st.markdown("### Predicción de gastos para el próximo mes")

	# Get prediction data from API
	prediction_data, error = get_predictions()

	if error:
		st.error(f"Error al obtener datos de predicción: {error}")
	else:
		# Extract prediction data
		client_id = prediction_data.get('client_id', 'N/A')
		predicted_amount = prediction_data.get('current_month_spend', 0)

		# Create columns for prediction display
		col_pred1, col_pred2 = st.columns([1, 1])

		with col_pred1:
			# Display prediction information
			st.markdown("""
			<div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; height: 120px; display: flex; flex-direction: column; justify-content: center;">
				<p style="color: #31333F; margin-bottom: 0.5rem; font-size: 1rem; font-weight: 600;">Predicción para el próximo mes</p>
				<p style="color: #31333F; margin-bottom: 0; font-size: 1.5rem; font-weight: 600;">💡 Basado en tu historial de gastos</p>
			</div>
			""", unsafe_allow_html=True)

		with col_pred2:
			# Display the predicted amount with styling
			st.markdown(f"""
			<div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; height: 120px; display: flex; flex-direction: column; justify-content: center;">
				<p style="color: #31333F; margin-bottom: 0.5rem; font-size: 1rem; font-weight: 600;">Gasto estimado</p>
				<p style="color: #31333F; margin-bottom: 0; font-size: 1.8rem; font-weight: 600;">${predicted_amount:,.2f}</p>
				<p style="color: #31333F; margin-top: 0.5rem; font-size: 0.8rem;">Esta predicción se basa en tu historial de transacciones y patrones de gasto.</p>
			</div>
			""", unsafe_allow_html=True)

		# Add some tips based on the prediction
		if predicted_amount > 0:
			# Get current month's spending from the spending trends data
			current_month_amount = 0
			if spending_trends and len(spending_trends) > 0:
				current_month_amount = spending_trends[-1].get('amount', 0)

			# Compare with current month's spending if available
			if current_month_amount > 0:
				percent_change = ((predicted_amount - current_month_amount) / current_month_amount) * 100
				if percent_change > 10:
					st.warning(f"⚠️ La predicción muestra un aumento del {percent_change:.1f}% en tus gastos para el próximo mes. Considera revisar tu presupuesto.")
				elif percent_change < -10:
					st.success(f"✅ ¡Buenas noticias! Se prevé una disminución del {abs(percent_change):.1f}% en tus gastos para el próximo mes.")
				else:
					st.info(f"ℹ️ Se prevé que tus gastos se mantengan estables para el próximo mes (variación del {percent_change:.1f}%).")
			else:
				st.info("ℹ️ Planifica tu presupuesto para el próximo mes basándote en esta predicción.")
