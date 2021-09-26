# Web tools imports
from logging import debug
import threading
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
        latest_update_id = int(tg_response["result"][-1]["update_id"])
        while tg_response["result"]:
            tg_response = requests.get(TG_API + "/getUpdates", params={"offset": latest_update_id + 1, "limit": 100, "timeout": 0}).json()
            if tg_response["result"]:
                latest_update_id = int(tg_response["result"][-1]["update_id"])
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
        if tg_response.get("result", {}):

            # Elaborate each update one by one
            for tg_update in tg_response["result"]:

                # Keep counting running "update manager" threads
                while True:
                    um_thread_n = 1

                    # Count running "update manager" threads
                    for thread in threading.enumerate():
                        if thread.name.startswith("um_thread-"):
                            um_thread_n += 1

                    # If there aren't more than 10 running "update manager" threads exit
                    if not um_thread_n > 10:
                        break

                    # Wait 0.1s before counting again
                    sleep(0.1)
                

                if DEBUG_PRINTS:
                    print("\n\nUpdate:\n" + str(tg_response) + "\n\nStarting thread n." + str(um_thread_n))

                # Elaborate update in another thread
                Thread(target=updates_manager, args=[tg_update], name="um_thread-" + str(um_thread_n)).start()


            latest_update_id = int(tg_response["result"][-1]["update_id"])


        # Wait half a second before checking for new updates
        sleep(0.5)