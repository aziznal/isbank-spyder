# TODO: recheck this entire script so it fits with the new file structure
# TODO: use project_settings.json to manage global settings instead of hardcoding them
from datetime import datetime
import json
import os
from time import sleep

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from BankSpyder import BankSpyder
from ResultGrapher import ResultGrapher
from EmailSender import EmailSender
import functions as fn

# TODO: find areas where exceptions may be raised and handle them so things stay nice and functional
# IDEA: design a GUI to use with the program at a (much) later time

# TODO: add a task in windows task scheduler to run the script everyday at 09:00


# region Data Getting
# spooder
special_options = FirefoxOptions()
special_options.headless = True

# BUG: 'special_options' should be refactored to 'options'. work on it and find any other mishaps. your past self was too tired.
spyder = BankSpyder("https://www.isbank.com.tr/en/foreign-exchange-rates", special_options=special_options)

print("Spyder is running..")

# required_point_freq = spyder.settings['dataPointFreq']

# interval = fn.set_new_interval(
#     spyder.settings['startingHour'],
#     spyder.settings['endingHour'],
#     required_point_freq
#     )

# TODO: delete later
required_point_freq = 21
interval = fn.set_new_interval(
    3,
    6,
    required_point_freq
)

print(f"Each loop will take approx. {round(interval * 60, 1)} minutes")

loop_count = 0

# creates a new data point every loop
while True:

    # Break Condition
    if loop_count == required_point_freq:
        break    

    print(f"Starting {fn.numth(loop_count)}/{required_point_freq} Loop")
    loop_count += 1

    current_time = fn.get_current_time()

    # scrippity scrape
    try:
        results = spyder.doYourThing()
        results["timestamp"] = spyder.get_timestamp()

        # path is used again in ResultGrapher
        results_folder_path = fn.save_scraped_data(spyder=spyder, results=results)

        # wait, refresh, then restart loop
        # IDEA: using built-in 'Display' button instead of refreshing page takes less time
        sleep(interval)
        spyder.refresh_page()

    except WebDriverException as e:
        print(f"Encountered Exception during Data Getting Stage: {e}")
        # TODO: handle exception properly before deployment
        # IDEA: include log in email if exception is found
        break

# endregion Data Getting

# region Graphing

print("\nFinished Scraping Sucessfully. Creating Graph..")
grapher = ResultGrapher(results_folder_path=results_folder_path)
grapher.create_graph(save=True, show=True)

print("Graph Created Sucessfully")

# endregion

# region Sending Email

email_settings = {

    "smtp_server": "smtp.gmail.com",
    "port": 587,

    "sender": "abodena3al@gmail.com",
    "sender_app_pass": "avytikqznhqcsegv",

    "receiver": "abodenaal@gmail.com",
    
    "subject": "Daily Exchange Rates"

}

sender = EmailSender(settings=email_settings)

sender.set_email_body("email_template.html", "I don't even know why this is here")
sender.set_attachment('graphing_results/2020-04-30.png')

sender.send_email()

# endregion

spyder.die()    # this method is better than burning your entire house
