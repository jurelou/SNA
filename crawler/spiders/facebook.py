# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
from crawler import config
from crawler.spiders import ISpider
from crawler.http import Request

logger = logging.getLogger('crawler')


class Facebook(ISpider):
    name = "facebook spider"

    def __init__(self):
        super().__init__()
        self.entrypoint = Request(
            "https://m.facebook.com",
            method="GET",
            callback=self.login,
            errback=self.error)

    def error(self, err):
        logger.fatal(f"In facebook spider: {err}")

    def login(self, res):
        login_data = {
            'email': config.FACEBOOK_CREDENTIALS[0],
            'pass': config.FACEBOOK_CREDENTIALS[1]}
        yield Request('https://m.facebook.com/login.php', method='POST', body=login_data, allow_redirects=False, callback=self.after_login, errback=self.error)

    def after_login(self, res):
        if 'c_user' not in res.cookies:
            logger.fatal(f"Facebook authentication failed")
            return
        logger.info(f"Facebook authentication succeeded!")
        yield Request('https://m.facebook.com/home.php', callback=self.home_page, errback=self.error)

    def home_page(self, res):
        print("@@@@@@@@@", res)