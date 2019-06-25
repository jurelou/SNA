# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging

logger = logging.getLogger('sna')


class Outcome():
    def __init__(self, data, request=None):
        self.data = data
        self.request = request

class OutcomeManager():
    def __init__(self):
        self.spider = None

    def start(self, spider):
        self.spider = spider

    def store(self, outcome):
        logger.info("OutcomeManager store()")

    def close(self):
        pass