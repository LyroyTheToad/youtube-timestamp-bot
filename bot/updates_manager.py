# Package imports
from bot import TG_API
# Web tools imports
import requests
# Other imports
import re

def updates_manager(tg_update):

    #
    #
    # Saving necessary info
    #
    #

    #
    # If it's a message
    #

    # Initializing variables to avoid future exceptions
    chat_id = None
    chat_type = None
    message_id = None
    message_text = None
    message_entities = None
    command = None


    # If the update is a message from a channel
    if "channel_post" in tg_update:
        channel_post = tg_update["channel_post"]

        chat_type = channel_post["chat"]["type"]


    # If the update is a message not from a channel
    elif "message" in tg_update:
        message = tg_update["message"]

        chat_id = message["chat"]["id"]
        chat_type = message["chat"]["type"]
        message_id = message["message_id"]
        message_text = message["text"]
        message_entities = message.get("entities", {})
        # Check if the message text contains only the command itself
        if (message_entities and message_entities[0]["type"] == "bot_command" and
            message_entities[0]["offset"] == 0 and len(message_text) == message_entities[0]["length"]
        ):
            # I know I could have used the <message_text> variable to store
            # the command but I decided not to to make everything more clear
            command = message_text






    #
    #
    # Elaborate data
    #
    #

    #
    # If the update comes from a chat
    #
    if chat_id:

        #
        # If the update comes from a private chat
        #

        if chat_type == "private":

            #
            # If the update is a command
            #

            if command:

                #
                # Start command
                #
                if command == "/start":
                    requests.get(TG_API + "/sendMessage", params={
                        "chat_id": chat_id,
                        "text": "tutorial"
                    })




                #
                # Help command
                #
                if command == "/help":
                    requests.get(TG_API + "/sendMessage", params={
                        "chat_id": chat_id,
                        "text": "tutorial"
                    })




            #
            # Else if the message follows the correct format (yt_link - HH:MM:SS)
            #
            elif re.search("^http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?\s-\s[0-5]?\d(:[0-5]\d){0,2}$", message_text):
                
                #
                # Send back modified link
                #

                message_text = message_text.split(" - ")