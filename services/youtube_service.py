import logging
import os
import json
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from utils.env_utils import get_env_variable

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

logging.basicConfig(level=logging.INFO,  # Adjust the level as needed
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])  # Logs to console

class YouTubeAnalyticsService:
    def __init__(self):
        # Set the required scope for YouTube Analytics API
        self.scopes = ["https://www.googleapis.com/auth/youtube","https://www.googleapis.com/auth/youtube.readonly","https://www.googleapis.com/auth/yt-analytics.readonly"]
        self.credentials = self.get_credentials()
        self.base_url = "https://youtubeanalytics.googleapis.com/v2"

    def get_credentials(self):
        """
        Handles OAuth2 authorization, either using saved tokens or initiating a new flow.
        """
        token_path = "credentials/token.json"
        creds = None

        # Load existing credentials from token file, if available
        if os.path.exists(token_path):
            with open(token_path, "r") as token_file:
                creds = Credentials.from_authorized_user_info(json.load(token_file), self.scopes)

        # If credentials are not valid or missing, start OAuth flow
        if not creds or not creds.valid:
            if creds and creds.refresh_token:
                logging.info("Inside if ")
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials/client_secrets.json", self.scopes
                )
                logging.info("Inside else ")
                flow.redirect_uri = "http://127.0.0.1:8000"
                creds = flow.run_local_server(port=8080, prompt="consent")
                logging.info(creds)

            # Save the credentials for future use
            with open(token_path, "w") as token_file:
                token_file.write(creds.to_json())
        # Check if refresh_token is missing
        if not creds.refresh_token:
            raise ValueError("No refresh token found. Delete token.json and re-authenticate.")

        return creds

    # def get_analytics_data(self, start_date: str, end_date: str, metrics: str, dimensions: str = None, filters: str = None):
    def get_analytics_data(self, start_date, end_date, metrics, dimensions=None, filters=None):
        url = "https://youtubeanalytics.googleapis.com/v2/reports"
        params = {
            "ids": "channel==MINE",
            "startDate": start_date,
            "endDate": end_date,
            "metrics": metrics
        }
        if dimensions:
            params["dimensions"] = dimensions
        if filters:
            params["filters"] = filters

        headers = {"Authorization": f"Bearer {self.credentials.token}"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
