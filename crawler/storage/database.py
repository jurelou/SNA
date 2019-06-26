# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
from crawler.storage import GraphDB
logger = logging.getLogger('sna')


class Database():
    def __init__(self):
        logger.info("New Database")
        self.graphDB = GraphDB()

    def start(self):
        logger.info("Start Database")    

    def store_relation(self, relation):
        self.graphDB.store(relation)

    def close(self):
        logger.info("Stop Database")
        self.graphDB.stop()