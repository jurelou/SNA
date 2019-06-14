# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

from twisted.internet import defer, reactor, task
from twisted.python import failure


def fail(_failure):
    d = defer.Deferred()
    reactor.callLater(0.1, d.errback, _failure)
    return d


def succeed(result):
    d = defer.Deferred()
    reactor.callLater(0.1, d.callback, result)
    return d
