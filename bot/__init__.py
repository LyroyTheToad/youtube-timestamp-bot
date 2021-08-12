# Other imports
import os
import json
# (Used during localhost testing to load the environment variables from .env files)
from dotenv import load_dotenv
load_dotenv()






#
#
# Updates that the bot will react to
#
#

ALLOWED_UPDATES = json.dumps([
    "message"
])






#
#
# Load environment variables
#
#

TOKEN = os.environ["TOKEN"]
DEBUG_PRINTS = bool(os.environ["DEBUG_PRINTS"])
# Set first part of the API request URL
TG_API = "https://api.telegram.org/bot" + TOKEN