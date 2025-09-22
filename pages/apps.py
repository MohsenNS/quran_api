# from django.apps import AppConfig
# from . import eitaa_selenium
# import threading

# class PagesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'pages'

#     def ready(self):
#         thread = threading.Thread(target=eitaa_selenium.start_bot)
#         thread.start()


from django.apps import AppConfig
from . import eitaa_selenium
import threading
import os
import atexit

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self):
        # Check if the code is running in the main process and not the reloader process
        if os.environ.get('RUN_MAIN', None) != 'true':
            print("Skipping bot start in reloader process.")
            return

        print("Starting the bot in the main process...")
        thread = threading.Thread(target=eitaa_selenium.start_bot)
        thread.daemon = True # Use a daemon thread
        thread.start()

        def close_browser():
            try:
                self.driver.quit()
                print("Closed Selenium on shutdown.")
            except Exception:
                pass

        atexit.register(close_browser)


# import os
# import threading
# from django.apps import AppConfig
# from . import eitaa_selenium

# class PagesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'pages'

#     def ready(self):
#         # if os.environ.get('RUN_MAIN') != 'true':
#         #     # Prevents execution during the initial runserver fork
#         #     return

#         print("Running start_bot() only once")
#         threading.Thread(target=eitaa_selenium.start_bot, daemon=True).start()


# import threading
# import traceback
# from django.apps import AppConfig
# from . import eitaa_selenium

# class PagesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'pages'

#     def ready(self):
#         def run_wrapper():
#             try:
#                 print("[BOT] start_bot() launching")  # visible in pm2 logs
#                 eitaa_selenium.start_bot()
#                 print("[BOT] start_bot() returned")
#             except Exception:
#                 print("[BOT] exception in start_bot():")
#                 traceback.print_exc()

#         threading.Thread(target=run_wrapper, daemon=True).start()

