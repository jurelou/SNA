# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
import requests
from requests_threads import AsyncSession
from crawler.http import Response
from twisted.internet import defer
from twisted.internet import reactor

logger = logging.getLogger('sna')


class Downloader():
    def __init__(self, crawler):
        logger.debug(f"New Downloader with spider {crawler.spider.name}")
        self.session = AsyncSession(n=100)
        self.crawler = crawler

    def download(self, request):
        logger.debug(f"DOWNLOADER downloading {request.method} {request.url}")
        if request.method == "GET":
            d = self.session.get(
                request.url,
                #params=request.params,
                allow_redirects=request.allow_redirects)
        elif request.method == "POST":
            d = self.session.post(
                request.url,
                #params=request.params,
                data=request.body,
                allow_redirects=request.allow_redirects)
        else:
            d = defer.Deferred()
            reactor.callLater(0, d.errback, ValueError(f"Undefined method found: {request.method}"))
            return d            
        return d.addCallback(self.send_response, request)

    def start(self):
        logger.debug("Starting Downloader")
        for c in self.crawler.spider.preload_cookies:
            logger.debug(f"Downloader adding preloading cookie: {c['name']} for {c['domain']}")
            cookie = requests.cookies.create_cookie(
                domain=c['domain'],
                name=c['name'],
                value=c['value'])
            self.session.cookies.set_cookie(cookie)

    @staticmethod
    def send_response(response, request):
        return Response(
            request=request,
            status=(
                response.status_code,
                response.reason),
            body=response.content,
            cookies=response.cookies,
            encoding=response.encoding,
            headers=response.headers,
            meta=request.meta
        )

    @staticmethod
    def is_busy():
        return False

    @staticmethod
    def close():
        logger.debug("Close Downloader")
