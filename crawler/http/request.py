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
            meta = None):
        self.url = url
        self._method = method
        self.callback = callback
        self.errback = errback
        self._body = body
        self._params = params
        self._cookies = cookies
        self.allow_redirects = allow_redirects
        self.meta = meta

    @property
    def method(self):
        return self._method
    
    @property
    def callback(self):
        return self._callback

    @property
    def body(self):
        return self._body

    @property
    def params(self):
        return self._params

    @property
    def cookies(self):
        return self._cookies

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
