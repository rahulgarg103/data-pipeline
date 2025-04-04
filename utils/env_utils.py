from dotenv import load_dotenv
import os

load_dotenv()

def get_env_variable(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value
