import requests
from utils.env_utils import get_env_variable

class FacebookService:
    def __init__(self):
        self.access_token = get_env_variable("FACEBOOK_PAGE_ACCESS_TOKEN")
        self.base_url = "https://graph.facebook.com/v22.0"

    def get_page_data(self, page_id: str):
       
        url = f"{self.base_url}/{page_id}/insights?metric=page_impressions_unique&access_token={self.access_token}"
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
