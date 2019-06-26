# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
from crawler import config

logger = logging.getLogger('sna')


class User():
    def __init__(self, data):
        self.data = data
        print("NEW USER WITH DATA", data)

class Relation():
    def __init__(self, _from, relation, to):
        self._from = _from
        self._relation = relation
        self._to = to

    def __str__(self):
    	return f"{self._from} -- {self._relation} --> {self._to}"