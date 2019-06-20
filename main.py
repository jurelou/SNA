import logging
from crawler.utils import initLogger
initLogger()
logging.getLogger('crawler').setLevel(logging.INFO)

from crawler.crawler import CrawlerManager
from crawler.spiders import Facebook
from crawler import config

config.test_config()
process = CrawlerManager()
process.crawl(Facebook())
process.start()
