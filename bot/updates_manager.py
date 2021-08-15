# Package imports
from bot import TG_API, DEBUG_PRINTS, MESSAGE_REGEX
# Web tools imports
import requests
import pafy
# Other imports
import re
from time import sleep

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
        print("\nmessage_text: " + str(message_text) + "\ncommand: " + str(command))


    



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

            # The while is used to retry in case of exception
            while True:

                # Try to make a requests to Telegram severs
                try:

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
                            "text": "You must use the format  `<YouTube link\> HH:MM:SS`\n\nExample:\nhttps://youtu\.be/dQw4w9WgXcQ 2:47\n\n",
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
                                    "This bot __DOES NOT__ save any data and __WILL NOT__ send you any ads\!\n\n" +
                                    "The creator of this bot is @Lyroy\_TheToad, if there are any problems with the bot or you want to request a feature fell free to ask me\.\n" +
                                    "You can find the code here https://github\.com/LyroyTheToad/youtube\-timestamp\-bot",
                                    "parse_mode": "MarkdownV2",
                                    "disable_web_page_preview": True
                        })

                # Retry if failed
                except:
                    sleep(10)
                    continue

                # Exit from while if succeeded
                break




    

        #
        # Else if it's a message that follows the correct format (YouTube_link - HH:MM:SS)
        #

        elif message_text and (groups := re.search(MESSAGE_REGEX, message_text)):

            #
            # Elaborate message
            #

            # Separate sections
            message_text = message_text.split(" ")
            video_id = groups.group(1)
            # If there are no parameters set it an empty string
            if not (link_params := groups.group(2)):
                link_params = ""
            starting_time = re.split(":", message_text[1])


            # Remove every "t" parameter
            while link_params and (t_param := re.search("&t=[^&]*", link_params)):
                link_params = link_params.replace(t_param.group(), "")


            # Check if the YouTube video exists
            while True:

                try:
                    video = pafy.new(video_id)
                except Exception as exc:

                    print (exc)
                    # If it failed connecting retry
                    if str(exc).find("[Errno 11001]") != -1:
                        continue

                    # If the video doesn't exist
                    elif str(exc).find("Video unavailable") != -1:
                        while True:
                            try:
                                requests.get(TG_API + "/sendMessage", params={
                                    "chat_id": chat_id,
                                    "text": "The sent link is not a valid YouTube link!"
                                })
                            except:
                                sleep(10)
                                continue
                            break
                        return

                # Exit from while if it succeeded
                break


            # Calculate time in seconds
            if len(starting_time) == 1:
                starting_time = int(starting_time[0])
            elif len(starting_time) == 2:
                starting_time = int(starting_time[0]) * 60 + int(starting_time[1])
            else:
                starting_time = int(starting_time[0]) * 60 * 60 + int(starting_time[1]) * 60 + int(starting_time[2])

            
            # Check if the specified starting time overflows the video duration
            if starting_time > video.length:
                while True:
                    try:
                        requests.get(TG_API + "/sendMessage", params={
                            "chat_id": chat_id,
                            "text": "The specified time overflows the duration of the video!"
                        })
                    except:
                        sleep(10)
                        continue
                    break
                return




            #
            # Send back modified link
            #
            while True:
                try:
                    requests.get(TG_API + "/sendMessage", params={
                        "chat_id": chat_id,
                        "text": "https://www.youtube.com/watch?v=" + video_id + "&t=" + str(starting_time) + link_params
                    })
                except:
                    sleep(10)
                    continue
                break

        




        #
        # Else (if the user has sent a random message)
        #

        else:
            while True:
                try:
                    requests.get(TG_API + "/sendMessage", params={
                        "chat_id": chat_id,
                        "text": "Send a message in the format  `<YouTube link\> HH:MM:SS `to get your modified YouTube link\!",
                        "parse_mode": "MarkdownV2"
                    })
                except:
                    sleep(10)
                    continue
                break
