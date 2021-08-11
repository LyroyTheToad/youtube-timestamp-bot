# Other imports
import os
# (Used during localhost testing to load the environment variables from .env files)
from dotenv import load_dotenv
load_dotenv()






#
#
# Load environment variables
#
#

TOKEN = os.environ["TOKEN"]
# Set first part of the API request URL
TG_API = "https://api.telegram.org/bot" + TOKEN