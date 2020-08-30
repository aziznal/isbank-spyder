from selenium.common.exceptions import *


class CurrencyNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TableNotFoundException(NoSuchElementException):
    def __init__(self, msg=None, screen=None, stacktrace=None):
        super().__init__(msg=msg, screen=screen, stacktrace=stacktrace)


class StalledSpyderException(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
