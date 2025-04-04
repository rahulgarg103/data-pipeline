import requests
from requests.auth import HTTPBasicAuth

from utils.env_utils import get_env_variable

class StripeService:
    def __init__(self):
        self.api_key = get_env_variable("STRIPE_API_KEY")
        self.base_url = "https://api.stripe.com/v1"

    def get_transaction_data(self):
        url = f"{self.base_url}/charges"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        # response = requests.get(url, headers=headers)
        response = requests.get(url, auth=HTTPBasicAuth(self.api_key, ''))

        response.raise_for_status()
        return response.json()
