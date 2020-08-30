from selenium import webdriver
import os
from time import sleep
import json
from datetime import datetime
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.options import Options


default_options = Options()
default_options.headless = True


class BasicSpider:
    def __init__(self, url, buffer_time=3, options=default_options, **kwargs):
        """ 
        Args:
        
            url (str): page to load when browser is first launched
            buffer_time (int, optional): a wait-time (in seconds) to allow things like page loads to finish. Defaults to 3.
            options (selenium.webdriver.firefox.options.Options, optional): Use to pass custom options to the browser.
        """

        self.buffer_time = buffer_time

        self._driver = webdriver.Firefox(options=options)
 
        self.goto(url)

        self.page_soup = self._load_page_soup()


    def _load_page_soup(self):
        return BeautifulSoup(self.page_source, features="lxml")

    @property
    def url(self):
        return self._driver.current_url

    @url.setter
    def url(self, _):
        raise TypeError("BaseSpyder.url is a read-only property")
    
    @property
    def page_source(self):
        return self._driver.page_source

    @page_source.setter
    def page_source(self, _):
        raise TypeError("BaseSpyder.page_source is a read-only property")

    def wait(self):
        sleep(self.buffer_time)

    def goto(self, url):
        self._driver.get(url)
        self.wait()

    def refresh_page(self):
        self._driver.refresh()
        self.wait()

        # refresh page source to get new changes
        self.page_soup = self._load_page_soup()


    def get_timestamp(self, for_filename=False):
        """
        returns a formatted timestamp string (e.g "2020-09-25 Weekday 16:45:37" )
        """
        if for_filename:
            formatted_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        else:
            formatted_time = datetime.now().strftime("%Y-%m-%d %A %H:%M:%S")

        return formatted_time

    def smooth_scroll(self, scroll_to, velocity):
        pass

    def instant_scroll(self, scroll_to):
        pass

    def slow_type(self, field, sentence, speed):
        pass

    def die(self):
        print("Squashing the spyder...")
        self._driver.quit()
