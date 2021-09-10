import os
import json
# (Used during localhost testing to load the environment variables from .env files)
from dotenv import load_dotenv
load_dotenv()




#
# Updates that the bot will react to
#

ALLOWED_UPDATES = json.dumps([
    "message"
])




#
# Regex for correctly formatted message
#

MESSAGE_REGEX = "^(?:https?:\/\/|\/\/)?(?:(?:www\.|m\.)?youtube(?:-nocookie)?\.com\/(?:(?:vi?|e|embed)\/([\w-]{11})|(?:watch|embed|attribution_link)?\?\S*?(?:(?<=\?v=|&v=)|(?<=\?vi=|&vi=))([\w-]{11}))|youtu\.be\/(?:([\w-]{11})(?!\S*v=)|\S*?(?:&v=|\?v=)([\w-]{11})))(?:[^\w\s-]\S*)?$"




#
# Load environment variables
#

TOKEN = os.environ["TOKEN"]
DEBUG_PRINTS = bool(os.environ["DEBUG_PRINTS"])
# Set first part of the API request URL
TG_API = "https://api.telegram.org/bot" + TOKEN