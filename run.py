# Web tools imports
import requests
# Package imports
from bot import TG_API, ALLOWED_UPDATES, DEBUG_PRINTS
from bot.updates_manager import updates_manager
# Other imports
from threading import Thread
from time import sleep

if __name__ == "__main__":

    # Ignore updates sent while the bot was off (max limit for "getUpdates" method is 100)
    # It's a really ugly and confusing way of doing it but I couldn't find a better one
    try:
        tg_response = requests.get(TG_API + "/getUpdates", params={"limit": 100, "timeout": 0, "allowed_updates": ALLOWED_UPDATES}).json()
        latest_update_id = int(tg_response["result"][0]["update_id"])
        while tg_response["result"]:
            tg_response = requests.get(TG_API + "/getUpdates", params={"offset": latest_update_id + 1, "limit": 100, "timeout": 0}).json()
            if tg_response["result"]:
                latest_update_id = int(tg_response["result"][0]["update_id"])
    except IndexError:
        latest_update_id = 0


    print("Bot started!")

    # Start polling
    while True:
        
        # Try to make a requests to Telegram severs
        try:
            tg_response = requests.get(TG_API + "/getUpdates", params={"offset": latest_update_id + 1, "limit": 5, "timeout": 60}).json()
        except:
            sleep(10)
            continue


        # If there are any updates
        if tg_response["result"]:

            if DEBUG_PRINTS:
                print("\n\nUpdate:\n" + str(tg_response))

            # Elaborate each update one by one
            for tg_update in tg_response["result"]:
                Thread(target=updates_manager, args=[tg_update]).start()

            latest_update_id = int(tg_response["result"][-1]["update_id"])


        sleep(0.5)