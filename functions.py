import os
from datetime import datetime
import json

# from ResultGrapher import ResultGrapher
# from EmailSender import EmailSender

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


def get_timestamp():
    filename_ = datetime.now().strftime("%d-%m-%y_%H:%M")

    return filename_


def already_exists(path_):
    return os.path.isfile(path_)


def format_tuple(data):
    """changes (1, 2, "b") into "1,2,b"

    Args:

    @param data (tuple): Tuple to convert into comma seperated string

    Returns comma seperated string of tuple items
    """
    return ",".join([str(item) for item in data])


def append_new_data(data, path_):

    with open(path_, 'a') as file_:
        file_.write(data + '\n')


def create_new_datafile(data, path_):

    with open(path_, 'w') as file_:
        file_.write("time,currency,selling,buying\n")
        file_.write(data + '\n')


def prep_data(data):
    timestamped_data = (get_timestamp(), *data)
    formatted_data = format_tuple(timestamped_data)

    return formatted_data


def save_data(new_data):
    """Appends new_data to results/results.csv.

    If results.csv doesn't already exist, this function creates it and adds column names (time,buying,selling)

    @param new_data (tuple): Tuple (time,buying,selling)
    """

    data_file = project_settings['results_path']

    formatted_data = prep_data(new_data)

    if already_exists(data_file):
        append_new_data(formatted_data, data_file)
    else:
        create_new_datafile(formatted_data, data_file)


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
