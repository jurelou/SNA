# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
import queue

logger = logging.getLogger('crawler')


class Scheduler(object):
    def __init__(self, crawler):
        logger.debug("New Scheduler")
        self.q = queue.Queue()
        self.crawler = crawler

    def start(self):
        logger.debug("Start Scheduler")

    def close(self):
        logger.debug("Close Scheduler")
        pass

    def enqueue_request(self, request):
        logger.debug(f"Pushing to scheduler request: {request.url} {request.meta}")
        self.q.put(request)
        return True

    def dequeue_request(self):
        if self.q.empty():
            logger.debug(f"Scheduler have nothing to pop!")
            return None
        res = self.q.get()
        logger.debug(f"Scheduler pop request: {res.url} {res.meta}")
        return res
