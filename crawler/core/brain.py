# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
from twisted.internet import defer
from twisted.internet import reactor, error
from crawler.core.scraper import Scraper
from crawler.http import Response, Request
from crawler.core.scheduler import Scheduler
from crawler.core.downloader import Downloader
from crawler.utils import OutcomeManager

logger = logging.getLogger('crawler')


class Brain(object):
    def __init__(self, crawler, close_callback):
        logger.debug('New Brain')
        self.spider = crawler.spider
        self.running = False
        self.closing = False
        self.entrypoint = self.spider.entrypoint
        self.inprogress = set()
        self.crawler = crawler
        self.close_callback = close_callback
        self.downloader = Downloader(crawler)
        self.scraper = Scraper(crawler)
        self.scheduler = Scheduler(crawler)
        self.outcomeManager = OutcomeManager()

    def start(self):
        self.scheduler.start()
        self.scraper.start(self.spider)
        self.downloader.start()
        self.outcomeManager.start(self.spider)
        reactor.callLater(0, self.next)

    @defer.inlineCallbacks
    def run(self):
        if self.running:
            raise "Already running"
        self.running = True
        self._closewait = defer.Deferred()
        yield self._closewait

    def try_close(self):
        logger.debug('Trying to close brain')
        if (self.closing and not self.inprogress) or self.scraper.try_close():
            logger.debug('Brain can be closed now')
            self.closing.callback(None)

    def next(self):
        logger.debug("Brain next Event loop !")
        while not self.is_busy():
            if not self.from_scheduler():
                break
        if self.entrypoint and not self.is_busy():
            self.crawl(self.entrypoint)
            self.entrypoint = None

    def is_busy(self):
        ret = not self.running or self.closing or self.downloader.is_busy() or self.scraper.is_busy()
        if ret:
            logger.debug("Brain is busy!")
        return ret

    def from_scheduler(self):
        request = self.scheduler.dequeue_request()
        logger.debug('Brain calling next request from scheduler')
        if not request:
            return None
        self.inprogress.add(request)
        d = self.downloader.download(request)
        d.addErrback(self.downloader_error)
        d.addCallback(self.scraper.enqueue_scrape, request)
        d.addErrback(self.scrapper_error)

        def _then(response):
            reactor.callLater(0, self.next)
            self.inprogress.remove(request)
            return response
        d.addBoth(_then)
        d.addBoth(lambda _: self.try_close())
        return d.addBoth(lambda _: reactor.callLater(0, self.next))

    def scrapper_error(self, err):
        logger.error(f"After scrapper.enqueue_scrape: {err}")
        return err

    def downloader_error(self, err):
        logger.error(f"After downloader.download: {err}")
        return err

    def crawl(self, request):
        logger.debug(f"Crawling for {request.url}")
        self.scheduler.enqueue_request(request)
        reactor.callLater(0, self.next)

    def store(self, outcome):
        self.outcomeManager.store(outcome)

    def close(self):
        logger.debug('Close Brain')
        pass

    def stop(self):
        logger.debug('Stop Brain')
        if not self.running:
            return
        self.running = False
        d = self.stop_all()
        return self._closewait.callback(None)

    def stop_all(self):
        if self.closing:
            return self.closing
        self.closing = defer.Deferred()
        self.try_close()
        d = self.closing
        d.addBoth(lambda _: self.downloader.close())
        d.addErrback(lambda _: logger.error(
            'ERROR in BRAIN after downloader.close'))
        d.addBoth(lambda _: self.scraper.close())
        d.addErrback(lambda _: logger.error(
            'ERROR in BRAIN after scraper.close'))
        d.addBoth(lambda _: self.scheduler.close())
        d.addErrback(lambda _: logger.error(
            'ERROR in BRAIN after scheduler.close'))

        d.addBoth(lambda _: self.outcomeManager.close())
        d.addErrback(lambda _: logger.error(
            f'ERROR in BRAIN after outcomeManager.close {_}'))

        d.addBoth(lambda _: self.close_callback())
        return d
