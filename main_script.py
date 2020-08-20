from time import sleep
import json
import traceback

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from functions import *
from custom_functions import *


project_settings = load_project_settings()

# spooder
spyder = make_spyder()


def run_script():

    global spyder

    loop_count = 128
    interval = create_new_loop_interval(9, 17, loop_count)

    print(f"New data will be collected every {interval} seconds")

    current_loop = 0

    # A new data point will be created at every loop
    while current_loop < loop_count:
    
        print(f"Starting Loop {current_loop + 1} / {loop_count}")
        current_loop += 1

        # scrippity scrape
        try:
            data = spyder.get_single_reading()
            save_data(data)

            sleep(interval)

            spyder.refresh_page()

        except WebDriverException as e:
            print(f"Encountered Exception during Data Getting Stage: {e}")
            # TODO: setup exception handling
            # IDEA: include log in email if exception is found


try: 
    run_script()

except Exception as e:
    print(f"Encountered exception while running script: {e}")
    traceback.print_exc()

finally:
    spyder.die()


# Create graph
# path_to_graph = create_graph(current_results_path)

# Send Email
# send_results_as_email(path_to_graph)

input("Program execution has finished. Press Enter to exit")
