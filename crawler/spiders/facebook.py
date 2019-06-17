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
        self.base_url = 'https://m.facebook.com'
        self.entrypoint = Request(
            "https://m.facebook.com",
            callback=self.login,
            errback=self.error)

    def error(self, err):
        logger.fatal(f"In facebook spider: {err}")

    def login(self, res):
        login_data = {
            'email': config.FACEBOOK_CREDENTIALS[0],
            'pass': config.FACEBOOK_CREDENTIALS[1]}

        def _logged_in(res):
            if 'c_user' not in res.cookies:
                logger.fatal(f"Facebook authentication failed")
                return
            logger.info(f"Facebook authentication succeeded!")
            yield Request('https://m.facebook.com/home.php', callback=self.get_fb_dtsg, errback=self.error)
            for req in self.parse_user_page("johndoe"):
                yield req
        yield Request('https://m.facebook.com/login.php', method='POST', body=login_data, allow_redirects=False, callback=_logged_in, errback=self.error)

    """
        Find the facebook CSRF token (which is a hidden input in the facebook status bar)
    """
    def get_fb_dtsg(self, res):
        self.fb_dtsg = res.body.xpath('//input[@name="fb_dtsg"]/@value')[0]

    def parse_user_page(self, userID):
        def extract_data(res):
            data = {'friends_link': None,
                'photos_link': None,
                'likes_link': None,
                'family': {},
                'living' : {},
                'work': {},
                'education': {},
                'life_events': {}
            }
            friends_link = res.body.xpath('//div/a[.="Friends"]')
            if friends_link: data['friends_link'] = friends_link[0].attrib['href']

            photos_link = res.body.xpath('//div/a[.="Photos"]')
            if photos_link: data['photos_link'] = photos_link[0].attrib['href']

            likes_link = res.body.xpath('//div/a[.="Likes"]')
            if likes_link: data['likes_link'] = likes_link[0].attrib['href']

            family = res.body.xpath('//div[@id="family"]/div/div/div/div/h3/a')
            data['family'] = [f.attrib['href'] for f in family]

            living = res.body.xpath('//div[@id="living"]/div/div/div/table/tr/td/div/a')
            data['living'] = [(i.text, i.attrib['href']) for i in living] 

            work = res.body.xpath('//div[@id="work"]/div/div/div/div/div/div/span/a')
            data['work'] = [(i.text, i.attrib['href']) for i in work]

            education = res.body.xpath('//div[@id="education"]/div/div/div/div/div/div/div/span/a')
            data['education'] = [(i.text, i.attrib['href']) for i in education]

            life_events = res.body.xpath('//div[@id="year-overviews"]/div/div/div/div/div/div/div/a')
            data['life_events'] = [(i.text, i.attrib['href']) for i in life_events]
            for req in self.extract_profile_data(data):
                yield req

        yield Request(f'https://m.facebook.com/{userID}', callback=extract_data)        

    def extract_profile_data(self, data):
        #yield Request(f'https://m.facebook.com/{userID}/friends', callback=self.parse_friends_page)
        print("@@", data)
        if data['photos_link']:
            yield Request(self.base_url + data['photos_link'], callback=self.extract_photos_data)

    """
        Response is the content from facebook user albums: http://m.facebook.com/{userId}/photos?lst=X
        This method will search for peoples (likes, comments, reactions) in all public pictures
    """
    def extract_photos_data(self, response):
        def extract_albums(page):
            albums = page.xpath('//span/a')
            for album in albums:
                print("Found album ->", album.text, album.attrib['href'])
        extract_albums(response.body)

        def then(res):
            extract_albums(res.body)
            next_page = res.body.xpath('//span[contains(text(), " More Albums")]/ancestor::a')
            if next_page:
                print("NIIIIIIIIce!! even more albums !!")
                yield Request(self.base_url + next_page[0].attrib['href'], callback=then)
            else:
                print("No more albums.")

        see_all = response.body.xpath('//a[contains(text(), "See All (")]')
        if see_all:
            print("NICE, we found more albums :)")
            yield Request(self.base_url + see_all[0].attrib['href'], callback=then)
        else:
            print("Only one album page to get !")

    def parse_friends_page(self, res):
        def extract_friends(page):
            friends = page.xpath('//td[@class="v s"]/a')
            if friends:
                for f in friends:
                    with open("toto.txt", "a+") as a:
                        a.write(f"FRIEND of tonald drump-> {f.attrib['href']}\n")
            else:
                print("No friends on this page, this should not happen !!!!!!")
        extract_friends(res.body)
        next_link = res.body.xpath('//div[@id="m_more_friends"]/a')
        if next_link:
            yield Request(self.base_url + next_link[0].attrib['href'], callback=self.parse_friends_page)
