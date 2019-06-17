# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
from crawler.http import Response
from twisted.internet import defer
from crawler.utils.defer import succeed, fail
from twisted.web import http
from requests_threads import AsyncSession

logger = logging.getLogger('crawler')


class Downloader(object):
    def __init__(self, crawler):
        logger.debug("New Downloader")
        self.session = AsyncSession(n=100)

    def download(self, request):
        logger.debug(f"DOWNLOADER downloading {request.method} {request.url}")
        if request.method is "GET":
            d = self.session.get(
                request.url,
                params=request.params,
                allow_redirects=request.allow_redirects)
        elif request.method is "POST":
            d = self.session.post(
                request.url,
                params=request.params,
                data=request.body,
                allow_redirects=request.allow_redirects)
        else:
            return fail(ValueError(f"Undefined method found: {request.method}"))
        return d.addCallback(self.send_response, request)

    def send_response(self, response, request):
        return Response(
            request=request,
            status=(
                response.status_code,
                response.reason),
            body=response.content,
            cookies=response.cookies,
            encoding=response.encoding,
            headers=response.headers,
        )

    def is_busy(self):
        return False

    def close(self):
        logger.debug("Close Downloader")
