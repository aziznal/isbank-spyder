import os
from datetime import datetime
import json

from ResultGrapher import ResultGrapher
from EmailSender import EmailSender

project_settings = {}


def load_project_settings():
    global project_settings
    with open('project_settings.json', 'r') as settings_json:
        project_settings = json.load(settings_json)
        return project_settings


def get_current_time():
    """Returns a dict with keys ['hour'] and ['minutes'] with int values"""
    current_time = datetime.now().strftime("%H-%M").split('-')

    return {
        'hour': int(current_time[0]),
        'minutes': int(current_time[1])
    }


def create_new_loop_interval(start_hour: int, stop_hour: int, loop_count: int = 20):

    """ returns a time (in seconds) given by the formula:

        [ (stop_hour - start_hour) * 60 * 60 ] / loop_count
    """

    total_available_time = (stop_hour - start_hour) * 60 * 60   # in seconds
    interval = total_available_time // loop_count

    return interval


def save_scraped_data(spyder, results):
    # TODO: save all data in a single file instead of multiple
    # path subfolder to save current session's data in.
    results_folder_path = project_settings['results_path'] + \
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


def create_graph(path_to_results):
    print("\nFinished Scraping Sucessfully. Creating Graph..")

    grapher = ResultGrapher(results_folder_path=path_to_results)
    path_to_graph = grapher.create_graph(save=True, show=False)    

    print("Graph Created Sucessfully")

    return path_to_graph


def send_results_as_email(path_to_graph):

    print("\nSending Results as Email")

    sender = EmailSender()

    sender.set_email_body("email_template.html",
                        "I don't even know why this is here")
    sender.set_attachment(
        project_settings['graphing_results_path'] + path_to_graph)

    sender.send_email()

    print("Email sent successfully")


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
