from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

from BankSpyder import BankSpyder


class IsbankSpyder(BankSpyder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Website's built-in button to refresh exchange rates w/o refreshing whole page
        self._display_button = self._driver.find_element_by_class_name(
            'dK_button1')

    def _get_exchange_rate_table(self):
        """returns table as bs4.BeautifulSoup object"""
        # TODO: update object name
        table = self.page_soup.find(
            name="div", attrs={'id': 'htmlDefaultTableCover'})
        return table

    def _get_row_value(self):
        # TODO: update object names
        try:
            currency = row.find('div', {'class': 'dK_Line_Item1'}).text[1:4]
            selling = row.find('div', {'class': 'dK_Line_Item2'}).text.strip()
            buying = row.find('div', {'class': 'dK_Line_Item3'}).text.strip()

            return currency, float(selling), float(buying)

        except Exception as e:
            print(f"Error in __get_row_value: {e}")

    def get_single_reading(self):
        """
        returns a dict with this structure

        {

            "currency_name": 

                {
                "buying": float,
                "selling": float 
                }
        }
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


if __name__ == "__main__":
    print("Please launch the file labeled main_script.py")
