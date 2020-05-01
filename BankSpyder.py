from bs4.element import Tag
from datetime import datetime
import json

from abc import ABCMeta, abstractmethod

from BaseSpyder import BaseSpyder


# TODO: write the following in docs:
#   After Inheriting this class, all you need to do is define the two abstract methods,
#   making sure to return the values in the proper structure. the rest is handled by
#   the filter_data method

class BankSpyder(BaseSpyder):
    ___metaclass__ = ABCMeta

    def __init__(self, url, load_buffer=3, options=None):
        super().__init__(url, load_buffer=load_buffer, options=options)

    def load_settings(self, filepath='spyder_settings.json'):
        """
        Loads spyder_settings.json (default name)
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
