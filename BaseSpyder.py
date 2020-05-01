from selenium import webdriver
import os
from time import sleep
import json
from datetime import datetime
from pprint import pprint
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.options import Options

class BaseSpyder:
    def __init__(self, url, load_buffer=3, options: Options = None):
        """
        @param url: url to scrape from.

        @param load_buffer: how long to wait in between things that need waiting between in.

        @param special_options: Special Options to pass to the browser (e.g headless mode, no-notification mode, etc..)
        """
        self.load_buffer = load_buffer
        self.url = url
        
        if options is not None:
            print("initializing headless browser...")
            self.driver = webdriver.Firefox(options=options)
            print("Successfully Initialized")

        else:
            self.driver = webdriver.Firefox()

        self.goto(self.url)

        self.page_source = BeautifulSoup(self.driver.page_source, features="lxml")

        self.__settings_path = ""   # Don't put this before self.settings
        self.settings = self.load_settings()

    def goto(self, url):
        self.driver.get(url)
        sleep(self.load_buffer)

    def refresh_page(self):
        self.driver.refresh()
        sleep(self.load_buffer)

        # refresh page source to get new changes
        self.page_source = BeautifulSoup(self.driver.page_source, features="lxml")

    def load_settings(self, filepath='spyder_settings.json'):
        """
        Loads spyder_settings.json (default name).
        returns spyder_settings as <dict> 
        """
        self.__settings_path = filepath

        with open(self.__settings_path) as spyder_settings_json:
            return json.load(spyder_settings_json)

    def save_settings(self):
        """
        saves the current running spyder settings.
        """
        try:

            with open(self.__settings_path, 'w') as spyder_settings_json:
                json.dump(self.settings, spyder_settings_json, indent=4)
                print(f"successfully saved data to {self.__settings_path}")

        except Exception as e:

            print(f"Warning! exception in spyder.save_settings: {e}\n\nAttempting to Save data somewhere else...")

            _filename = 'spyder_settings_fallback' + self.get_timestamp(appending_to_file_name=True) + '.txt'
            with open(_filename, 'a') as _file:
                _file.write(str(self.settings))

                print(f"successfully saved data to {_filename}")

    def get_timestamp(self, appending_to_file_name=False):
        """
        returns a formatted timestamp string (e.g "2020-09-25 Weekday 16:45:37" )
        """
        if appending_to_file_name:
            formatted_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        else:
            formatted_time = datetime.now().strftime("%Y-%m-%d %A %H:%M:%S")

        return formatted_time

    def die(self):
        print("Squashing the spyder...")
        self.save_settings()
        self.driver.quit()
