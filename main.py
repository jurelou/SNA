from crawler.utils import initLogger
initLogger()

from crawler.crawler import CrawlerManager
from crawler.spiders import Facebook
from crawler import config

config.test_config()
process = CrawlerManager()
process.crawl(Facebook())
process.start()
