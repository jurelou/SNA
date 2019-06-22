# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import os
import pickle

class ISpider():
    lxml = False

    def __init__(self, name=None):
        self.cookies_file = os.path.dirname(
            os.path.realpath(__file__)) + "/.auth_cookies"
        if not hasattr(self, 'name'):
            raise ValueError("Spider must have a name")

    @property
    def preload_cookies(self):
        exists = os.path.exists(self.cookies_file)
        if not exists:
            return {}
        with open(self.cookies_file, 'rb') as f:
            try:
                cookies = pickle.load(f)
                return cookies[self.name]
            except EOFError:
                return {}

    def set_preload_cookies(self, value):
        exists = os.path.exists(self.cookies_file)
        cookies = {}
        if not hasattr(value, "__len__"):
            raise ValueError(f'Preload cookies need an iterable, found {type(value)}')
        for v in value:
            if not all(k in v for k in ("name", "value", "domain")):
                raise ValueError(f'Preload cookies need an object with name, \
                    value and domain keys, found{value}')
        if exists:
            with open(self.cookies_file, 'rb') as f:
                try:
                    cookies = pickle.load(f)
                except EOFError:
                    pass
        if self.name in cookies:
            del cookies[self.name]
        cookies[self.name] = value
        with open(self.cookies_file, 'wb') as f:
            pickle.dump(cookies, f)
