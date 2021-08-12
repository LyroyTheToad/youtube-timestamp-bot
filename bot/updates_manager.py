# Package imports
from bot import TG_API, DEBUG_PRINTS
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

    message = tg_update["message"]

    chat_id = message["chat"]["id"]
    chat_type = message["chat"]["type"]
    message_text = message.get("text", {})
    message_entities = message.get("entities", {})
    # Check if the message text contains only the command itself
    if (message_entities and message_entities[0]["type"] == "bot_command" and
        message_entities[0]["offset"] == 0 and len(message_text) == message_entities[0]["length"]
    ):
        # I know I could have used the <message_text> variable to store
        # the command but I decided not to to make everything more clear
        command = message_text
    else:
        command = None





    
    #
    #
    # Debug info
    #
    #

    if DEBUG_PRINTS:
        print("\nchat_id: " + str(chat_id) + "\nchat_type: " + str(chat_type) + "\nmessage_text: " + str(message_text) + "\ncommand: " + str(command))






    #
    #
    # Elaborate data
    #
    #

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
                            "❗️*IMPORTANT*❗️\n" +
                            "The bot __DOES NOT__ check if the timestamp overflows the duration of the video\!",
                    "parse_mode": "MarkdownV2",
                    "disable_web_page_preview": True
                })




            #
            # About command
            #

            elif command == "/about":
                requests.get(TG_API + "/sendMessage", params={
                    "chat_id": chat_id,
                    "text": "This bot was made because you can't copy a link that starts a video at a certain time using the official YouTube mobile app\." +
                            "Please use this bot only if you are from a mobile device and not from Desktop to reduce traffic\.\n" +
                            "❗️*IMPORTANT*❗️\n" +
                            "The bot __DOES NOT__ check if the timestamp overflows the duration of the video\!\n" +
                            "This bot __DOES NOT__ save any data and __WILL NOT__ send you any ads\!\n\n" +
                            "The creator of this bot is @Lyroy_TheToad, if there are any problems with the bot or you want to request a feature fell free to ask me\.\n" +
                            "You can find the code here https://github\.com/LyroyTheToad/youtube\-timestamp\-bot",
                            "parse_mode": "MarkdownV2",
                            "disable_web_page_preview": True
                })






        #
        # Else if it's a message that follows the correct format (YouTube_link - HH:MM:SS)
        #

        elif message_text and re.search("^http(?:s?):\/\/(?:(?:www|m)\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?\s\d?\d(:[0-5]\d){0,2}$", message_text):

            #
            # Elaborate message
            #

            # Separate sections
            message_text = message_text.split(" ")
            yt_link = message_text[0]
            time = re.split(":", message_text[1])

            # Calculate time in seconds
            if len(time) == 1:
                time = int(time[0])
            elif len(time) == 2:
                time = int(time[0]) * 60 + int(time[1])
            else:
                time = int(time[0]) * 24 * 60 + int(time[1]) * 60 + int(time[2])




            #
            # Check for link type
            #

            # If it's a short link
            if yt_link.find("/watch?v=") == -1:

                # Send back modified link
                requests.get(TG_API + "/sendMessage", params={
                    "chat_id": chat_id,
                    "text": yt_link + "?t=" + str(time)
                })

            # If it's a long link
            else:
                
                # Send back modified link
                requests.get(TG_API + "/sendMessage", params={
                    "chat_id": chat_id,
                    "text": yt_link + "&t=" + str(time)
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