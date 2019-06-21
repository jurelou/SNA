# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
import lxml.html
from collections import deque
from twisted.python.failure import Failure
from twisted.internet import defer, task, reactor
from crawler.utils.defer import succeed
from crawler.http import Request, Response
from crawler.utils import Outcome

logger = logging.getLogger('crawler')


class Scraper(object):
    def __init__(self, crawler):
        logger.debug("New Scrapper")
        self.max_concurency = 100
        self.spider = None
        self.queue = deque()
        self.queue_in_progress = set()
        self.crawler = crawler

    def start(self, spider):
        self.spider = spider

    def is_busy(self):
        if len(self.queue) > self.max_concurency:
            logger.debug("SCRAPPER is busy right now")
            return True
        return False

    def close(self):
        logger.debug("Close Scrapper")
        return

    def try_close(self):
        ret = not (self.queue or self.queue_in_progress)
        if ret:
            logger.debug("SCRAPPER can be closed")
        return ret

    def enqueue_scrape(self, response, request):
        d = defer.Deferred()
        self.queue.append((response, request, d))

        def _then(_):
            self.queue_in_progress.remove(request)
            self.try_close()
            self.next()
            return _
        d.addBoth(_then)
        self.next()
        return d

    def next(self):
        while self.queue:
            response, request, deferred = self.pop_next()
            if response and request.callback:
                self.call_spider(response, request).chainDeferred(deferred)

    def pop_next(self):
        response, request, deferred = self.queue.popleft()
        self.queue_in_progress.add(request)
        return response, request, deferred

    def call_spider(self, response, request):
        d = defer.Deferred()
        if isinstance(response, defer.Deferred):
            d = response
        elif isinstance(response, Failure):
            reactor.callLater(0, d.errback, response)
        else:
            reactor.callLater(0, d.callback, response)

        def format_response(response):
            if not self.spider.lxml or not response.body:
                return response
            logger.debug("Formating response with LXML")
            response.body = lxml.html.fromstring(response.body)
            return response
        d.addCallback(format_response)
        d.addCallback(request.callback)
        d.addCallback(self.handle_spider_output, request, response)
        d.addErrback(logger.fatal, "ERROR in spider callback function:")
        return d

    def handle_spider_error(self, err, request, response):
        logger.fatal(f"ERROR in SCRAPPER from spider request: {request.url} {err}")
        self.crawler.brain.stop()

    def iter(self, iterable, errback, request, response):
        it = iter(iterable)
        while True:
            try:
                yield next(it)
            except StopIteration:
                break
            except Exception:
                errback(Failure(), request, response)

    def handle_spider_output(self, res, request, response):
        if res is None:
            return succeed(None)
        elif not isinstance(res, (dict, bytes)) and hasattr(res, '__iter__'):
            pass
        else:
            res = [res]
        it = self.iter(res, self.handle_spider_error, request, response)
        coop = task.Cooperator()
        work = (self.from_spider(output, request, response) for output in it)
        return defer.DeferredList([coop.coiterate(work)
                                   for _ in range(self.max_concurency)])

    def from_spider(self, output, request, response):
        if isinstance(output, Request):
            logger.debug(f"SCRAPER got request from spider: {output.url}")
            self.crawler.brain.crawl(output)
        elif isinstance(output, Outcome):
            logger.debug(f"SCRAPER got outcome for request: {request.url}")
            self.crawler.brain.store(output)
        elif output is None:
            logger.debug("SCRAPER got EMPTY request from spider")
            pass
        else:
            logger.fatal(f"ERROR in SCRAPPER got strange spider output {output}")
