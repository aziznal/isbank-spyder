from time import sleep
import json

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from IsbankSpyder import IsbankSpyder
from ResultGrapher import ResultGrapher
from EmailSender import EmailSender
import functions as fn


project_settings = fn.load_project_settings()

# spooder
special_options = FirefoxOptions()
special_options.headless = False

url = "https://www.isbank.com.tr/en/foreign-exchange-rates"

spyder = IsbankSpyder(url=url, options=special_options)

loop_count = 600
interval = fn.create_new_loop_interval(start_hour=0,
                                       stop_hour=1,
                                       loop_count=loop_count)

current_loop = 0

# A new data point will be created at every loop
while True:

    # Break Condition
    if current_loop == loop_count:
        break

    print(f"Starting Loop {current_loop + 1} / {loop_count}")
    current_loop += 1

    current_time = fn.get_current_time()

    # scrippity scrape
    try:
        results = spyder.filter_data()
        results["timestamp"] = spyder.get_timestamp()

        # path is used again in ResultGrapher
        # FIXME: This variable is being reassigned every loop for no reason..
        current_results_path = fn.save_scraped_data(
            spyder=spyder, results=results)

        sleep(interval)

        spyder.refresh_page()

    except WebDriverException as e:
        print(f"Encountered Exception during Data Getting Stage: {e}")
        # TODO: handle exception properly before deployment
        # IDEA: include log in email if exception is found    ___metaclass__ = ABCMeta

# Create graph
path_to_graph = fn.create_graph(current_results_path)

# Send Email
fn.send_results_as_email(path_to_graph)

#   TODO: kill spyder as soon as loop is finished instead of later
### Exceptions may arise that prevent this code from being executed
spyder.die()    # this method is better than burning your entire house
