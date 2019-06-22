# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
import signal
from twisted.internet import reactor, defer
from crawler.core.brain import Brain

logger = logging.getLogger('crawler')


class Crawler():
    def __init__(self, spider):
        logger.info(f'New Crawler with spider: {spider.name}')
        self.spider = spider
        self.brain = Brain(self, self.stop)

    @defer.inlineCallbacks
    def crawl(self):
        logger.debug(f'Starting to crawl for {self.spider.name}')
        try:
            yield self.brain.start()
            yield defer.maybeDeferred(self.brain.run)
        except Exception as e:
            logger.fatal(f'Error in crawling: {e}', exc_info=True)
            if self.brain is not None:
                yield self.brain.close()

    @defer.inlineCallbacks
    def stop(self):
        logger.debug('Stop crawler')
        yield defer.maybeDeferred(self.brain.stop)


class CrawlerManager():
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.crawlers = set()
        self.deffered_crawlers = set()

    @defer.inlineCallbacks
    def join(self):
        while self.deffered_crawlers:
            yield defer.DeferredList(self.deffered_crawlers)

    def signal_handler(self, sig, frame):
        logger.fatal('You pressed Ctrl+C!')
        reactor.callFromThread(self.stop)

    def crawl(self, spider):
        crawler = Crawler(spider)
        self.crawlers.add(crawler)
        d = crawler.crawl()
        self.deffered_crawlers.add(d)

        def _then(result):
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            self.crawlers.discard(crawler)
            self.deffered_crawlers.discard(d)
            return result
        return d.addBoth(_then)

    def start(self):
        d = self.join()
        if d.called:
            return
        d.addBoth(self.stop)
        tp = reactor.getThreadPool()
        tp.adjustPoolsize(maxthreads=42)
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False)

    def stop(self, *args, **kwargs):
        logger.debug('CRAWLERMANAGER stop')
        d = defer.DeferredList([c.stop() for c in list(self.crawlers)])

        def stop_reactor(res):
            try:
                reactor.stop()
            except RuntimeError:
                pass
            return defer.succeed(res)
        return d.addBoth(stop_reactor)
