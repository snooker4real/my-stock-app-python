import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Alpha Vantage API Key
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError("API_KEY not found in .env file")
