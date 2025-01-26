import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

if not API_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found")

if not SPOONACULAR_API_KEY:
    raise ValueError("SPOONACULAR_API_KEY not found")