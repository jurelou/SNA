# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

from crawler.http import Request


class Response(object):
    def __init__(
            self,
            status=(
                4242,
                "default status"),
            headers=None,
            body=None,
            request=None,
            cookies=None,
            encoding=None):
        self._status = status
        self._body = body
        self._headers = headers
        self._cookies = cookies
        self.request = request
        self.encoding = encoding

    def __str__(self):
        ret = f"\nRequest: {self._status}\nrequest: {self.request.url}\nHeaders:\n\t"
        for h in self._headers:
            ret += f"{h} -> {self._headers[h]}\n\t"
        ret += "\nCookies:\n\t"
        for c in self._cookies:
            ret += f"{c.name} -> {c.value} ({c.domain})\n\t"
        return ret

    @property
    def status(self):
        return self._status

    @property
    def cookies(self):
        return self._cookies

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def headers(self):
        return self._headers

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, value):
        if not isinstance(value, Request) and value is not None:
            raise ValueError('Inappropriate type: {} for response.request whereas a Request \
            is expected'.format(type(value)))
        self._request = value