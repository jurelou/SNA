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


class Scheduler():
    def __init__(self, crawler):
        logger.debug("New Scheduler")
        self.q = queue.Queue()
        self.seen_requests = set()
        self.crawler = crawler

    @staticmethod
    def start():
        logger.debug("Start Scheduler")

    @staticmethod
    def close():
        logger.debug("Close Scheduler")

    def enqueue_request(self, request):
        if hash(request) in self.seen_requests:
            logger.debug(f"Request : {request.url} {request.meta} have already been requested.")
            return False
        logger.debug(f"Pushing to scheduler request: {request.url} {request.meta}")
        self.q.put(request)
        self.seen_requests.add(hash(request))
        return True

    def dequeue_request(self):
        if self.q.empty():
            logger.debug(f"Scheduler have nothing to pop!")
            return None
        res = self.q.get()
        logger.debug(f"Scheduler pop request: {res.url} {res.meta}")
        return res
