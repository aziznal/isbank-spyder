from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

from selenium.common.exceptions import *

from BankSpider import BankSpider
from CustomExceptions import *


class IsbankSpider(BankSpider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._refresh_button = self._get_refresh_button()

        # NOTE: Page html changes after clicking refresh, so it must be done first
        self.refresh_page()

    def _get_refresh_button(self):
        # Page is refreshed using internal button for better load speeds
        button_ = self._driver.find_element_by_class_name('dK_button1')
        return button_

    def refresh_page(self):
        self._refresh_button.click()
        self.page_soup = self._load_page_soup()

    @staticmethod
    def _check_table_is_not_none(table):
        if table is None:
            msg = "Table of Exchange Rates was not found"
            raise TableNotFoundException(msg)

    def _get_table_rows(self):

        tag = 'table'
        tag_attrs = {"class": "dk_MT"}

        table = self.page_soup.find(tag, tag_attrs)

        self._check_table_is_not_none(table)

        rows = self._extract_table_rows(table)

        return rows

    def _extract_table_rows(self, table: BeautifulSoup):

        table_rows = table.findChildren(name="tr", recursive=False)

        # Skip first row since it's just column names
        table_rows = table_rows[1:]

        return table_rows

    def _extract_values(self, row: BeautifulSoup):

        row_children = row.findAll(recursive=False)

        currency = self._get_currency(row_children[0])
        bank_buys = self._get_rate(row_children[1])
        bank_sells = self._get_rate(row_children[2])
        
        return currency, bank_buys, bank_sells

    @staticmethod
    def _get_currency(value: BeautifulSoup):
        extracted_value = value.text.strip().split(' ')[0]
        return extracted_value

    @staticmethod
    def _get_rate(value):
        extracted_value = value.text.strip()
        return float(extracted_value)

    @staticmethod
    def _get_usd(values):

        currency_ = 'USD'

        for value in values:
            if value[0] == currency_:
                return value

        raise CurrencyNotFoundException(f"The currency {currency_} was not found in the scraped results")

    
    def get_single_reading(self):
        
        rows = self._get_table_rows()
        extracted_values = [self._extract_values(row) for row in rows]

        usd_row = self._get_usd(extracted_values)

        return usd_row
