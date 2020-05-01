# TODO: set this up to it's more of a general spyder for all others to inherit from
from bs4.element import Tag
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import json

from BaseSpyder import BaseSpyder


class BankSpyder(BaseSpyder):

    def __init__(self, url, load_buffer=3, options=None):
        super().__init__(url, load_buffer=load_buffer, options=options)

        # Website's built-in button to refresh exchange rates w/o refreshing
        self.display_button = self.driver.find_element_by_class_name('dK_button1')


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

    def __getExchangeRateTable(self):
        """returns table as bs4.BeautifulSoup object"""
        table = self.page_source.find(name="div", attrs={'id': 'htmlDefaultTableCover'})
        return table

    def doYourThing(self):
        """
        returns { currency: { buying: float, selling: float }}
        """

        table = self.__getExchangeRateTable()

        super_dict = dict()

        for row in table:
            # example row value: 'USD, Sold @ 6.7702 , Bought @ 7.1147'
            row_val = self.__getRowValue(row)
            super_dict[row_val[0]] = {
                'selling': row_val[1],
                'buying':  row_val[2]
            }

        return super_dict

    def __getRowValue(self, row: Tag):
        # region row structure
        # each row is a div made up of the following divs:

        # div.dK_Line_Item1
        #   <img ...>
        #   ABC                     ************
        #   <span>...</span>

        # div.dK_Line_Item2
        #   current sell price      ************

        # div.dK_Line_Item3
        #   current buy price       ************
        # endregion row structure

        try:
            currency = row.find('div', {'class': 'dK_Line_Item1'}).text[1:4]
            selling = row.find('div', {'class': 'dK_Line_Item2'}).text.strip()
            buying = row.find('div', {'class': 'dK_Line_Item3'}).text.strip()

            return currency, float(selling), float(buying)

        except Exception as e:
            print(f"Error in getRowValue: {e}")

    def get_timestamp(self, appending_to_file_name=False):
        """
        returns a formatted timestamp string (e.g "2020-09-25 Weekday 16:45:37" )
        """
        if appending_to_file_name:
            formatted_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        else:
            formatted_time = datetime.now().strftime("%Y-%m-%d %A %H:%M:%S")

        return formatted_time

    def refresh_page(self):
        self.display_button.click()
        sleep(self.load_buffer / 2)

        # must reassign page source to get new changes
        self.page_source = BeautifulSoup(self.driver.page_source, features="lxml")
