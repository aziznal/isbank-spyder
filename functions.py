import os
from datetime import datetime
import json
import sys
from time import sleep

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from IsbankSpider import IsbankSpider

project_settings = {}


def make_spider(url):
    
    options = FirefoxOptions()
    options.headless = False

    # TODO: replace with an instance of your bank spider
    spider = IsbankSpider(url=url, options=options)

    return spider


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


def get_current_day():
    """
    Returns nonabbreviated lowercase current day. e.g. saturday | monday
    """
    current_day = datetime.now().strftime('%A').lower()
    return current_day


def banks_are_closed():
    
    current_time = get_current_time()['hour']
    current_day = get_current_day()

    conditions = [
        current_day == 'saturday',
        current_day == 'sunday',
        current_time < 9,
        current_time > 18
    ]

    return any(conditions)


def banks_are_open():
    today = get_current_day()
    current_time = get_current_time()

    conditions = [
        today != 'saturday',
        today != 'sunday',
        current_time['hour'] < 18,
        current_time['hour'] >= 9
    ]

    return all(conditions)


def sleep_until_banks_open():
    today = get_current_day()
    current_time = get_current_time()

    while banks_are_closed():

        sameline_print('Waiting for banks to open..')
        sleep(1)

    return


def create_new_loop_interval(start_hour: int, stop_hour: int, loop_count: int = 20):
    """ returns a time (in seconds) given by the formula:

        [ (stop_hour - start_hour) * 60 * 60 ] // loop_count
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
    """ (1, 2, 'b') -> '1,2,b' """
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

    If results.csv doesn't already exist, this function creates it and adds column names (time,currency,buying,selling)

    @param new_data (tuple): Tuple (time,currency,buying,selling)
    """

    data_file = project_settings['results_path']

    formatted_data = prep_data(new_data)

    if already_exists(data_file):
        append_new_data(formatted_data, data_file)
    else:
        create_new_datafile(formatted_data, data_file)


def scrape(spyder, interval):
    data = spyder.get_single_reading()
    save_data(data)

    sleep(interval)

    spyder.refresh_page()


def sameline_print(output):
    sys.stdout.write('\r' + output)


def make_ascii_spyder():
    print(f'''
           ;               ,           
         ,;                 '.         
        ;:                   :;        
       ::                     ::       
       ::                     ::       
       ':                     :        
        :.                    :        
     ;' ::                   ::  '     
    .'  ';                   ;'  '.    
   ::    :;                 ;:    ::   
   ;      :;.             ,;:     ::   
   :;      :;:           ,;"      ::   
   ::.      ':;  ..,.;  ;:'     ,.;:   
    "'"...   '::,::::: ;:   .;.;""'    
        '"""....;:::::;,;.;"""         
    .:::.....'"':::::::'",...;::::;.   
   ;:' '""'"";.,;:::::;.'""""""  ':;   
  ::'         ;::;:::;::..         :;  
 ::         ,;:::::::::::;:..       :: 
 ;'     ,;;:;::::::::::::::;";..    ':.
::     ;:"  ::::::"""'::::::  ":     ::
 :.    ::   ::::::;  :::::::   :     ; 
  ;    ::   :::::::  :::::::   :    ;  
   '   ::   ::::::....:::::'  ,:   '   
    '  ::    :::::::::::::"   ::       
       ::     ':::::::::"'    ::       
       ':       """""""'      ::       
        ::                   ;:        
        ':;                 ;:"        
-hrr-     ';              ,;'          
            "'           '"            
              '

    ''')

