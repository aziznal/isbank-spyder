from bs4.element import Tag
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

from BankSpyder import BankSpyder

class IsbankSpyder(BankSpyder):

    def __init__(self, url, load_buffer=3, options=None):
        super().__init__(url, load_buffer=load_buffer, options=options)

        # Website's built-in button to refresh exchange rates w/o refreshing
        self.display_button = self.driver.find_element_by_class_name('dK_button1')

    # overridden
    def __get_exchange_rate_table(self):
        """returns table as bs4.BeautifulSoup object"""
        table = self.page_source.find(name="div", attrs={'id': 'htmlDefaultTableCover'})
        return table

    # overridden
    def __get_row_value(self, row: Tag):
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
            print(f"Error in __get_row_value: {e}")

    def refresh_page(self):
        self.display_button.click()
        sleep(self.load_buffer / 2)

        # must reassign page source to get new changes
        self.page_source = BeautifulSoup(self.driver.page_source, features="lxml")

    def filter_data(self):
        """
        returns { currency: { buying: float, selling: float }}
        """

        table = self.__get_exchange_rate_table()

        super_dict = dict()

        for row in table:
            # example row value: 'USD, Sold @ 6.7702 , Bought @ 7.1147'
            row_val = self.__get_row_value(row)
            super_dict[row_val[0]] = {
                'selling': row_val[1],
                'buying':  row_val[2]
            }

        return super_dict
