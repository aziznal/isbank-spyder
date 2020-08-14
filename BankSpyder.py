from datetime import datetime
import json

from BaseSpyder import BaseSpyder


# TODO: write the following in docs:
#   After Inheriting this class, all you need to do is define the two abstract methods,
#   making sure to return the values in the proper structure. the rest is handled by
#   the filter_data method

class BankSpyder(BaseSpyder):
    ___metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
