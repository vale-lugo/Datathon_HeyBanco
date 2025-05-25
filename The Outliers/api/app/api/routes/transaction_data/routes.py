from app.api.routes.transaction_data.resources import transaction_data_namespace
from app.api.routes.transaction_data.monthly_report import register_monthly_report_routes
from app.api.routes.transaction_data.category_spending import register_category_spending_routes
from app.api.routes.transaction_data.search import register_search_routes
from app.api.routes.transaction_data.recent import register_recent_routes
from app.api.routes.transaction_data.statistics import register_statistics_routes


def register_transaction_data_namespace(rest_api):
	# Register the main namespace
	rest_api.add_namespace(transaction_data_namespace)

	# Register sub-routes
	register_monthly_report_routes()
	register_category_spending_routes()
	register_search_routes()
	register_recent_routes()
	register_statistics_routes()
