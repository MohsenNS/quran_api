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

# Global flag to track if bot has started
bot_started = False

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self):
        global bot_started
        
        # Prevent multiple starts
        if bot_started:
            return
            
        # Check if we're running under PM2 or in main process
        is_pm2 = 'PM2' in os.environ or 'PM2_HOME' in os.environ
        is_main_process = os.environ.get('RUN_MAIN') == 'true' or not os.environ.get('DJANGO_AUTO_RELOAD', True)
        
        if not is_pm2 and not is_main_process:
            print("Skipping bot start in reloader process.")
            return

        print("Starting the bot in the main process...")
        thread = threading.Thread(target=eitaa_selenium.start_bot)
        thread.daemon = True
        thread.start()
        
        bot_started = True  # Set flag to prevent future starts

# from django.apps import AppConfig
# from . import eitaa_selenium
# import threading
# import os

# class PagesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'pages'

#     def ready(self):
#         # Check if the code is running in the main process and not the reloader process
#         if os.environ.get('RUN_MAIN', None) != 'true':
#             print("Skipping bot start in reloader process.")
#             return

#         print("Starting the bot in the main process...")
#         thread = threading.Thread(target=eitaa_selenium.start_bot)
#         thread.daemon = True # Use a daemon thread
#         thread.start()


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

