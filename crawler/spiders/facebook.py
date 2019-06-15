# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging
from crawler.utils.webbrowser import open_page
from crawler import config
from crawler.spiders import ISpider
from crawler.http import Request

logger = logging.getLogger('crawler')


class Facebook(ISpider):
    name = "facebook spider"
    lxml = True

    def __init__(self):
        super().__init__()
        self.fb_dtsg = None
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

        def go_home_page(res):
            if 'c_user' not in res.cookies:
                logger.fatal(f"Facebook authentication failed")
                return
            logger.info(f"Facebook authentication succeeded!")
            yield Request('https://m.facebook.com/home.php', callback=self.get_profile, errback=self.error)
        yield Request('https://m.facebook.com/login.php', method='POST', body=login_data, allow_redirects=False, callback=go_home_page, errback=self.error)

    def get_profile(self, res):
        self.fb_dtsg = res.body.xpath('//input[@name="fb_dtsg"]/@value')[0]
        yield Request('https://m.facebook.com/donald.trump.144', callback=self.parse_profile)

    def parse_profile(self, res):
        open_page(res)