# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

from crawler.http import Request


class ISpider(object):
    def __init__(self):
        if not hasattr(self, 'name'):
            raise ValueError("Spider must have a name")
