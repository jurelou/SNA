# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

import logging, os
from crawler import config
from crawler.spiders import ISpider
from crawler.http import Request
from crawler.utils import Outcome, open_page
from crawler.spiders.Facebook import albums
logger = logging.getLogger('crawler')


class Facebook(ISpider):
    name = "facebook spider"
    lxml = True

    def __init__(self):
        super().__init__()
        self.fb_dtsg = None
        self.base_url = 'https://m.facebook.com'
        self.entrypoint = Request(
            "https://m.facebook.com",
            callback=self.try_login,
            errback=self.error)
        self.start_user = "margot.laval.9"

    def error(self, err):
        logger.fatal(f"In facebook spider: {err}")

    def login(self, response):
        if not all(k in response.cookies for k in ('c_user', 'xs', 'sb')):
            logger.fatal(f"Facebook authentication failed")
            return
        logger.info(f"Facebook authentication succeeded!")
        preload_cookies = []
        for c in response.cookies:
            if c.name in ['c_user', 'xs', 'sb']:
                preload_cookies.append(
                    {'name': c.name, 'value': c.value, 'domain': c.domain})
        self.set_preload_cookies(preload_cookies)
        for req in self.parse_user_page(self.start_user):
            yield req

    def try_login(self, res):
        def is_logged_in(response):
            csrf_token = self.fb_dtsg = res.body.xpath(
                '//input[@name="fb_dtsg"]/@value')
            if not csrf_token:
                logger.info("Need to loggin to facebook")
                login_data = {
                    'email': config.FACEBOOK_CREDENTIALS[0],
                    'pass': config.FACEBOOK_CREDENTIALS[1]}
                yield Request('https://m.facebook.com/login.php', method='POST', body=login_data, allow_redirects=False, callback=self.login, errback=self.error)
            else:
                logger.info(
                    "Already logged in to facebook thanks to the preloaded cookies")
                for req in self.parse_user_page(self.start_user):
                    yield req
        yield Request('https://m.facebook.com/home.php', callback=is_logged_in)

    def parse_user_page(self, userID):
        def extract_data(res):
            data = {'user': res.meta['user'],
                    'friends_link': None,
                    'photos_link': None,
                    'likes_link': None,
                    'family': {},
                    'living': {},
                    'work': {},
                    'education': {},
                    'life_events': {}
                    }
            friends_link = res.body.xpath('//div/a[.="Friends"]')
            if friends_link:
                data['friends_link'] = friends_link[0].attrib['href']

            photos_link = res.body.xpath('//div/a[.="Photos"]')
            if photos_link:
                data['photos_link'] = photos_link[0].attrib['href']

            likes_link = res.body.xpath('//div/a[.="Likes"]')
            if likes_link:
                data['likes_link'] = likes_link[0].attrib['href']

            family = res.body.xpath('//div[@id="family"]/div/div/div/div/h3/a')
            data['family'] = [f.attrib['href'] for f in family]

            living = res.body.xpath(
                '//div[@id="living"]/div/div/div/table/tr/td/div/a')
            data['living'] = [(i.text, i.attrib['href']) for i in living]

            work = res.body.xpath(
                '//div[@id="work"]/div/div/div/div/div/div/span/a')
            data['work'] = [(i.text, i.attrib['href']) for i in work]

            education = res.body.xpath(
                '//div[@id="education"]/div/div/div/div/div/div/div/span/a')
            data['education'] = [(i.text, i.attrib['href']) for i in education]

            life_events = res.body.xpath(
                '//div[@id="year-overviews"]/div/div/div/div/div/div/div/a')
            data['life_events'] = [(i.text, i.attrib['href'])
                                   for i in life_events]
            for req in self.extract_profile_data(data):
                yield req
        yield Request(f'https://m.facebook.com/{userID}', callback=extract_data, meta={"user": userID})

    def extract_profile_data(self, data):
        # yield Request(f'https://m.facebook.com/{userID}/friends',
        # callback=self.parse_friends_page)
        if data['photos_link']:
            yield Request(self.base_url + data['photos_link'], callback=albums.extract_albums_data, meta={'user': data['user']})
    """
    def parse_friends_page(self, res):
        def extract_friends(page):
            friends = page.xpath('//td[@class="v s"]/a')
            if friends:
                for f in friends:
                    #print("Found friend:", f.attrib['href'], f.attrib)
                    pass
            else:
                #print("No friends on this  page, this should not happen !!!!!!")
                pass
        extract_friends(res.body)
        next_link = res.body.xpath('//div[@id="m_more_friends"]/a')
        if next_link:
            yield Request(self.base_url + next_link[0].attrib['href'], callback=self.parse_friends_page)
    """
