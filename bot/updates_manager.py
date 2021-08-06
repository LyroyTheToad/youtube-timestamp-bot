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
                        "text": "Send a message in the format  `<YouTube link\> HH:MM:SS `to get your modified YouTube link\!",
                        "parse_mode": "MarkdownV2"
                    })




                #
                # Help command
                #

                elif command == "/help":
                    requests.get(TG_API + "/sendMessage", params={
                        "chat_id": chat_id,
                        "text": "You must use the format  `<YouTube link\> HH:MM:SS`\n\nExample:\nhttps://youtu\.be/dQw4w9WgXcQ 2:47\n\n"+
                                "❗️*IMPORTANT*❗️\nThe bot __DOES NOT__ check if the timestamp overflows the duration of the video\!",
                        "parse_mode": "MarkdownV2",
                        "disable_web_page_preview": True
                    })




                #
                # About command
                #

                elif command == "/about":
                    requests.get(TG_API + "/sendMessage", params={
                        "chat_id": chat_id,
                        "text": "This bot was made because you can't copy a link that starts a video at a certain time using the official YouTube mobile app." +
                                "Please use this bot only if you are from a mobile device and not from Desktop to reduce traffic.\n\n" +
                                "The creator of this bot is @Lyroy_TheToad, if there are any problems with the bot or you want to request a feature fell free to ask me.1n" +
                                "You can find the code here https://github.com/LyroyTheToad/youtube-timestamp-bot"
                    })






            #
            # Else if it's a message that follows the correct format (yt_link - HH:MM:SS)
            #

            elif re.search("^http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?\s[0-5]?\d(:[0-5]\d){0,2}$", message_text):
                
                #
                # Send back modified link
                #

                # Elaborate message
                message_text = message_text.split(" ")
                yt_link = message_text[0]
                time = re.split(":", message_text[1])
                if len(time) == 1:
                    time = int(time[0])
                elif len(time) == 2:
                    time = int(time[0]) * 60 + int(time[1])
                else:
                    time = int(time[0]) * 24 * 60 + int(time[1]) * 60 + int(time[2])

                # Send response
                requests.get(TG_API + "/sendMessage", params={
                    "chat_id": chat_id,
                    "text": yt_link + "?t=" + str(time)
                })

            




            #
            # Else (if the user has sent a random message)
            #

            else:
                requests.get(TG_API + "/sendMessage", params={
                    "chat_id": chat_id,
                    "text": "Send a message in the format  `<YouTube link\> HH:MM:SS `to get your modified YouTube link\!",
                    "parse_mode": "MarkdownV2"
                })