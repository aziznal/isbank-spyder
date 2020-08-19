from time import sleep
import json

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from IsbankSpyder import IsbankSpyder
import functions as fn
import custom_functions as c_fn


project_settings = fn.load_project_settings()

# spooder

spyder = c_fn.make_spyder()

loop_count = 1
interval = 6
# interval = fn.create_new_loop_interval(start_hour=0, stop_hour=1, loop_count=loop_count)

print(f"Each interval will take {interval} seconds")

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
        results = spyder.get_single_reading()
        # results["timestamp"] = spyder.get_timestamp()

        # path is used again in ResultGrapher
        # FIXME: This variable gets reassigned every loop for no reason
        # current_results_path = fn.save_scraped_data(spyder=spyder, results=results)

        sleep(interval)

        spyder.refresh_page()

    except WebDriverException as e:
        print(f"Encountered Exception during Data Getting Stage: {e}")
        # TODO: handle e_extract_table_rowsly before deployment
        # IDEA: include log in email if exception is found

# Create graph
# path_to_graph = fn.create_graph(current_results_path)

# Send Email
# fn.send_results_as_email(path_to_graph)

#   TODO: kill spyder as soon as loop is finished instead of later
### Exceptions may arise that prevent this code from being executed
spyder.die()    # this method is better than burning your entire house
