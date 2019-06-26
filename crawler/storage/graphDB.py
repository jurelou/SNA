# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
from neo4j import GraphDatabase
from crawler import config

logger = logging.getLogger('sna')


class GraphDB():
    def __init__(self):
        driver = GraphDatabase.driver(config.NEO4J_CREDENTIALS[0], auth=(config.NEO4J_CREDENTIALS[1], config.NEO4J_CREDENTIALS[2]))
        self.session = driver.session()
        logger.info("New GraphDB")
    
    def store(self, relation):
        print("----------- ", relation)

    def close(self):
        self.session.close()
        logger.info("close GraphDB")        