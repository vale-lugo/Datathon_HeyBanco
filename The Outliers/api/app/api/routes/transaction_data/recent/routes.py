# Import resources to ensure they are registered with the namespace
from app.api.routes.transaction_data.recent.resources import RecentTransactionsResource

def register_recent_routes():
    # This function doesn't need to do anything as the routes are registered
    # with the namespace when the resources are imported
    pass