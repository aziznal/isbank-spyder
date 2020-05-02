# TODO: recheck this entire script so it fits with the new file structure
# TODO: use project_settings.json to manage global settings instead of hardcoding them
from time import sleep
import json

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from IsbankSpyder import IsbankSpyder
from ResultGrapher import ResultGrapher
from EmailSender import EmailSender
import functions as fn

from time import sleep

from progress.bar import ChargingBar as Bar


# TODO: find areas where exceptions may be raised and handle them so things stay nice and functional
# IDEA: design a GUI to use with the program at a (much) later time
# TODO: implement something like a progress bar to show the scraping progress insteed of whatever you have now
# TODO: add a task in windows task scheduler to run the script everyday at 09:00

# Load global project settings
project_settings = fn.load_project_settings()

# region Data Getting
# spooder
special_options = FirefoxOptions()
special_options.headless = True

spyder = IsbankSpyder("https://www.isbank.com.tr/en/foreign-exchange-rates", options=special_options)

print("Spyder is running..")

# required_point_freq = spyder.settings['dataPointFreq']

# interval = fn.set_new_interval(
#     spyder.settings['startingHour'],
#     spyder.settings['endingHour'],
#     required_point_freq
#     )

# TODO: delete later
required_point_freq = 10
interval = 10

interval /= 100  # dividing interval to be able to advance progress bar

print(f"Each loop will take approx. {interval} seconds")

loop_count = 0

# creates a new data point every loop
while True:

    # Break Condition
    if loop_count == required_point_freq:
        break    

    print(f"Starting {fn.numth(loop_count + 1)}/{required_point_freq}")
    loop_count += 1

    current_time = fn.get_current_time()

    # scrippity scrape
    try:
        results = spyder.filter_data()
        results["timestamp"] = spyder.get_timestamp()

        # path is used again in ResultGrapher
        current_results_path = fn.save_scraped_data(spyder=spyder, results=results)

        # wait, refresh, then restart loop
        bar = Bar('Waiting for next step', max=100, suffix='%(percent)d%%')
        
        for _ in range(100):
            sleep(interval)
            bar.next()

        bar.finish()

        spyder.refresh_page()

    except WebDriverException as e:
        print(f"Encountered Exception during Data Getting Stage: {e}")
        # TODO: handle exception properly before deployment
        # IDEA: include log in email if exception is found
        break

# endregion Data Getting

# region Graphing

print("\nFinished Scraping Sucessfully. Creating Graph..")
grapher = ResultGrapher(results_folder_path=current_results_path)
grapher.create_graph(save=True, show=True)

print("Graph Created Sucessfully")

# endregion

# region Sending Email

print("\nSending Results as Email")

sender = EmailSender()

sender.set_email_body("email_template.html", "I don't even know why this is here")
sender.set_attachment('graphing_results/2020-05-01.png')

sender.send_email()

print("Results sent successfully")

# endregion

spyder.die()    # this method is better than burning your entire house
