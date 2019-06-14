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
#from twisted.python.failure import Failure
logger = logging.getLogger('crawler')


class Downloader(object):
    def __init__(self, crawler):
        logger.debug("New Downloader")
        self.session = AsyncSession(n=100)
    """
    @defer.inlineCallbacks
    def make_a_request(self, request):

        response = yield treq.request(request.method, request.url, json=request.body, params=request.params, cookies=request.cookies)
        print("@@@@@@@@")
        if response.code == http.OK:
            result = yield response
        else:
            print("OPS")
            message = yield response

            raise Exception("Got an error from the server: {}".format(message))
        defer.returnValue(result)
    def get_content(self, response, request):
        d = treq.text_content(response)

        def forge_response(body, response, request):
            return Response(status=response.code, headers=response.headers, body=body, request=request, cookies=response.cookies())
        return d.addCallback(forge_response, response, request)
    """

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
