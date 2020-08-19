from selenium.common.exceptions import *
from custom_functions import *


class TableNotFoundException(NoSuchElementException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CurrencyNotFoundException(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    redirect_message()
