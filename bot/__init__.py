# Web tools imports
from flask import Flask
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

PORT = os.environ["PORT"]
TOKEN = os.environ["TOKEN"]
# Set first part of the API request URL
TG_API = "https://api.telegram.org/bot" + TOKEN







#
#
# Create Flask app
#
#

app = Flask(__name__)

from bot import routes