# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------


class Request(object):
    def __init__(
            self,
            url,
            method='GET',
            callback=None,
            errback=None,
            body=None,
            params=None,
            cookies=None,
            allow_redirects=True,
            meta=None):
        self.url = url
        self.method = method
        self.callback = callback
        self.errback = errback
        self.body = body
        self.params = params
        self.cookies = cookies
        self.allow_redirects = allow_redirects
        self.meta = meta

    def __eq__(self, other):
        return self.url == other.url and self.method == other.method and self.body == other.body and self.params == other.params and self.allow_redirects == other.allow_redirects

    def __hash__(self):
        return hash(
            (self.url,
             self.method,
             self.body,
             self.params,
             self.allow_redirects))

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, value):
        if value is not None and not callable(value):
            raise ValueError(f'Inappropriate type: {type(value)} for reqoest.callback whereas a function \
            is expected')
        else:
            self._callback = value

    @property
    def errback(self):
        return self._errback

    @errback.setter
    def errback(self, value):
        if value is not None and not callable(value):
            raise ValueError(
                f'Inappropriate type: {type(value)} for request.errback whereas a function is expected')
        else:
            self._errback = value
