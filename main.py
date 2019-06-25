# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

from crawler.utils import initLogger
from crawler.crawler import CrawlerManager
from crawler.spiders import Facebook
from crawler import config

initLogger()

if __name__ == "__main__":
    config.test_config()
    process = CrawlerManager()
    process.crawl(Facebook())
    process.start()
