# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

from crawler.http import Request


def extract_album_likes(response):
    def extract_likes(response):
        likes = response.body.xpath('//table/tbody/tr/td/div/h3/a')
        for like in likes:
            print(response.meta, like.text, like.attrib["href"])
        see_more = response.body.xpath('//li/table/tbody/tr/td/div/a')
        if see_more:
            yield Request('https://mbasic.facebook.com' + see_more[0].attrib['href'], callback=extract_likes, meta=response.meta)
    all_reactions = response.body.xpath(
        '//table/tbody/tr/td/div/div/a')[0].attrib['href']
    yield Request('https://mbasic.facebook.com' + all_reactions, callback=extract_likes, meta=response.meta)


def extract_album_data(response):
    likes = response.body.xpath(
        '//div[@id="root"]/table/tbody/tr/td/div/div/div/div/div/div/a')
    pictures = response.body.xpath('//div[@id="thumbnail_area"]/a')
    more_pictures = response.body.xpath('//div[@id="m_more_item"]/a')
    if likes:
        yield Request('https://mbasic.facebook.com' + likes[0].attrib['href'], callback=extract_album_likes, meta=response.meta)


def extract_albums_data(response):
    def extract_albums(res):
        albums = res.body.xpath('//span/a')
        for album in albums:
            yield Request('https://m.facebook.com' + album.attrib['href'], callback=extract_album_data, meta=dict({'album': album.text}, **res.meta))

    def goto_nextpage(res):
        for req in extract_albums(res):
            yield req
        next_page = res.body.xpath(
            '//span[contains(text(), " More Albums")]/ancestor::a')
        if next_page:
            yield Request('https://m.facebook.com' + next_page[0].attrib['href'], callback=goto_nextpage, meta=res.meta)

    see_all = response.body.xpath('//a[contains(text(), "See All (")]')
    if see_all:
        yield Request('https://m.facebook.com' + see_all[0].attrib['href'], callback=goto_nextpage, meta=response.meta)
    else:
        for req in extract_albums(response):
            yield req
