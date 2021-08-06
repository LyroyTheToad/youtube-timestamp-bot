# Package imports
from bot import TOKEN, app
from bot.updates_manager import *
# Web tools imports
from flask import request, abort
# Other imports
from threading import Thread






#
#
# Telegram updates route
#
#

@app.route("/" + TOKEN, methods=["GET", "POST"])
def get_updates():

    # If the request is HTTP POST
    if request.method == "POST":

        # Start thread
        Thread(target=updates_manager, args=[request.get_json()]).start()

        return "ok", 200


    # If the request isn't valid
    else:
        abort(404)






#
#
# Main route
#
#

@app.route("/")
def no():
    return "no", 200