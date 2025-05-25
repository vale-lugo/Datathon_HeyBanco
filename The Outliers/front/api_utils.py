import requests
import streamlit as st

# API base URL
API_BASE_URL = "http://31.97.12.162:8100/api"

def login(username, password):
    """
    Authenticate user with the API
    """
    url = f"{API_BASE_URL}/authentication/login"
    try:
        response = requests.post(url, json={"username": username, "password": password})
        if response.status_code == 200:
            try:
                data = response.json()
                # Store the access token in session state
                st.session_state['access_token'] = data.get('access_token')
                return True, None
            except ValueError:
                return False, "Invalid response from server (could not parse JSON)"
        else:
            try:
                error_data = response.json()
                error_msg = error_data.get('error', 'Authentication failed')
            except ValueError:
                # If response is not valid JSON
                error_msg = f"Authentication failed (Status code: {response.status_code})"
            return False, error_msg
    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, str(e)

def logout():
    """
    Logout user from the API
    """
    url = f"{API_BASE_URL}/authentication/logout"
    try:
        # Use the token if available
        headers = {}
        if 'access_token' in st.session_state:
            headers['Authorization'] = f"Bearer {st.session_state['access_token']}"

        response = requests.post(url, headers=headers)
        # Clear the token from session state
        if 'access_token' in st.session_state:
            del st.session_state['access_token']
        return True, None
    except Exception as e:
        return False, str(e)

def get_user_info():
    """
    Get information about the current user
    """
    url = f"{API_BASE_URL}/authentication/me"
    try:
        # Use the token if available
        if 'access_token' not in st.session_state:
            return None, "Not authenticated"

        headers = {'Authorization': f"Bearer {st.session_state['access_token']}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('error', 'Failed to get user info')
            return None, error_msg
    except Exception as e:
        return None, str(e)

def get_client_data():
    """
    Get client data for the current user
    """
    url = f"{API_BASE_URL}/client_data"
    try:
        # Use the token if available
        if 'access_token' not in st.session_state:
            return None, "Not authenticated"

        headers = {'Authorization': f"Bearer {st.session_state['access_token']}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('error', 'Failed to get client data')
            return None, error_msg
    except Exception as e:
        return None, str(e)

def get_transactions(page=1, per_page=10):
    """
    Get transaction data for the current user
    """
    url = f"{API_BASE_URL}/transaction_data?page={page}&per_page={per_page}"
    try:
        # Use the token if available
        if 'access_token' not in st.session_state:
            return None, "Not authenticated"

        headers = {'Authorization': f"Bearer {st.session_state['access_token']}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('error', 'Failed to get transaction data')
            return None, error_msg
    except Exception as e:
        return None, str(e)

def get_category_spending(start_date=None, end_date=None):
    """
    Get category spending data for the current user
    """
    url = f"{API_BASE_URL}/transaction_data/category_spending"
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date

    try:
        # Use the token if available
        if 'access_token' not in st.session_state:
            return None, "Not authenticated"

        headers = {'Authorization': f"Bearer {st.session_state['access_token']}"}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('error', 'Failed to get category spending data')
            return None, error_msg
    except Exception as e:
        return None, str(e)

def get_statistics(months=12):
    """
    Get transaction statistics for the current user
    """
    url = f"{API_BASE_URL}/transaction_data/statistics"
    params = {'months': months}

    try:
        # Use the token if available
        if 'access_token' not in st.session_state:
            return None, "Not authenticated"

        headers = {'Authorization': f"Bearer {st.session_state['access_token']}"}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('error', 'Failed to get statistics data')
            return None, error_msg
    except Exception as e:
        return None, str(e)

def get_monthly_report():
    """
    Get monthly transaction report data for the current user
    """
    url = f"{API_BASE_URL}/transaction_data/monthly_report"

    try:
        # Use the token if available
        if 'access_token' not in st.session_state:
            return None, "Not authenticated"

        headers = {'Authorization': f"Bearer {st.session_state['access_token']}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('error', 'Failed to get monthly report data')
            return None, error_msg
    except Exception as e:
        return None, str(e)

def get_predictions():
    """
    Get expense predictions for the next month for the current user
    """
    url = f"{API_BASE_URL}/predictions"

    try:
        # Use the token if available
        if 'access_token' not in st.session_state:
            return None, "Not authenticated"

        headers = {'Authorization': f"Bearer {st.session_state['access_token']}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json(), None
        else:
            error_msg = response.json().get('error', 'Failed to get prediction data')
            return None, error_msg
    except Exception as e:
        return None, str(e)

def register(username, password, client_id):
    """
    Register a new user with the API
    """
    url = f"{API_BASE_URL}/authentication/register"
    try:
        response = requests.post(url, json={"username": username, "password": password, "client_id": client_id})
        if response.status_code == 201:  # Assuming 201 Created for successful registration
            try:
                data = response.json()
                return True, None
            except ValueError:
                return False, "Invalid response from server (could not parse JSON)"
        else:
            try:
                error_data = response.json()
                error_msg = error_data.get('error', 'Registration failed')
            except ValueError:
                # If response is not valid JSON
                error_msg = f"Registration failed (Status code: {response.status_code})"
            return False, error_msg
    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {str(e)}"
    except Exception as e:
        return False, str(e)
