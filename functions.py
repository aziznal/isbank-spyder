import os
from datetime import datetime
import json


def get_current_time():
    """Returns a dict with keys ['hour'] and ['minutes'] with <int> as their values"""
    current_time = datetime.now().strftime("%H-%M").split('-')

    return {
        'hour': int(current_time[0]),
        'minutes': int(current_time[1])
    }


def set_new_interval(starting_hour: int, ending_hour: int, required_freq: int = 20):
    """
    returns: <int> seconds to wait between scrapes

    @param starting_hour: when scraper should start.

    @param ending_hour: when scraper should stop.

    @param required_freq: needed point frequency on graph.
    """

    # total seconds available between in given interval
    total_available_time = (ending_hour - starting_hour) * 60 * 60

    interval = total_available_time // required_freq

    return interval


def save_scraped_data(spyder, results):
    # path subfolder to save current session's data in.
    results_folder_path = os.getcwd() + "\\results\\" + \
        spyder.get_timestamp(appending_to_file_name=True).split(' ')[0]     # subfolder name only includes year-day-month

    # if this is the first loop cycle, this creates the subfolder
    if not os.path.isdir(results_folder_path):
        os.mkdir(results_folder_path)
        spyder.settings['currentFileIndex'] = 0     # reset at every new folder

    # IDEA: write code that won't make 'future you' cringe
    # save in json
    results_file_name = "\\result_" + str(spyder.settings['currentFileIndex']) + "_" + \
                        spyder.get_timestamp(appending_to_file_name=True).split(' ')[1] + \
                        ".json"

    with open(results_folder_path + results_file_name, "w") as result_file:
        json.dump(results, result_file, indent=4)
        spyder.settings['currentFileIndex'] += 1

    return results_folder_path

def numth(number):
    """
    returns a number followed by a proper 'th' e.g: 21 -> "21st"
    """
    if number <= 10:
        if number == 1:
            return str(number) + "st"
        if number == 2:
            return str(number) + "nd"
        if number == 3:
            return str(number) + "rd"
        # default case
        else:
            return str(number) + "th"
    if 10 < number <= 20:
        return str(number) + "th"
    else:
        if number % 10 == 1:
            return str(number) + "st"
        if number % 10 == 2:
            return str(number) + "nd"
        if number % 10 == 3:
            return str(number) + "rd"
        else:
            return str(number) + "th"