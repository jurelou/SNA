# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

from crawler.utils.webbrowser import open_page
from crawler.http import Request


def extract_likes(response):
    def extract(response):
        likes = response.body.xpath('//table/tbody/tr/td/div/h3/a')
        for like in likes:
            if like.text:
                # TODO: store result
                print("++++", response.meta, like.text, like.attrib["href"])
            pass
        see_more = response.body.xpath('//li/table/tbody/tr/td/div/a')
        if see_more:
            yield Request('https://mbasic.facebook.com' + see_more[0].attrib['href'], callback=extract, meta=response.meta)

    all_reactions = response.body.xpath('//table/tbody/tr/td/div/div/a')
    if all_reactions:
        yield Request('https://mbasic.facebook.com' + all_reactions[0].attrib['href'], callback=extract, meta=response.meta)
    else:
        for req in extract(response):
            yield req


def extract_picture_data(response):
    likes = response.body.xpath(
        '//div[@id="MPhotoContent"]/div/div[not(@class="msg")]/div/div/a')
    if likes:
        yield Request('https://mbasic.facebook.com' + likes[0].attrib['href'], callback=extract_likes, meta=dict({'likes_from': 'album.picture'}, **response.meta))
    comments = response.body.xpath(
        '//div[@id="MPhotoContent"]/div/div[not(@class="msg")]/div/div/div/div/h3/a')
    comments_like = response.body.xpath('//div/div/div/span/span/a')
    """
        comment_text = response.body.xpath('//div[@id="MPhotoContent"]/div/div[not(@class="msg")]/div/div/div/div/div[not(@class="mUFICommentContent")]/text()')
        print("->>>>", comment_text)
    """
    for comment in comments:
        print("!!!", response.meta, comment.text, comment.attrib['href'])
    for like in comments_like:
        yield Request('https://mbasic.facebook.com' + like.attrib['href'], callback=extract_likes, meta=dict({'likes_from': 'album.picture.comment'}, **response.meta))


def extract_album_data(response):
    likes = response.body.xpath(
        '//div[@id="root"]/table/tbody/tr/td/div/div/div/div/div/div/a')
    comments = response.body.xpath(
        '//tr/td/div/div/div/div/div/div/div/div/h3/a')
    comments_like = response.body.xpath('//div/div/div/div/span/span/a')

    def goto_next_pictures_page(response):
        pictures = response.body.xpath('//div[@id="thumbnail_area"]/a')
        for picture in pictures:
            yield Request('https://mbasic.facebook.com' + picture.attrib['href'], callback=extract_picture_data, meta=response.meta)
        more_pictures = response.body.xpath('//div[@id="m_more_item"]/a')
        if more_pictures:
            yield Request('https://mbasic.facebook.com' + more_pictures[0].attrib['href'], callback=goto_next_pictures_page, meta=response.meta)
    for req in goto_next_pictures_page(response):
        yield req
    if likes:
        yield Request('https://mbasic.facebook.com' + likes[0].attrib['href'], callback=extract_likes, meta=dict({'likes_from': 'album'}, **response.meta))
    for comment in comments:
        # TODO: store result
        print("@@@", response.meta, comment.text, comment.attrib['href'])
    for like in comments_like:
        yield Request('https://mbasic.facebook.com' + like.attrib['href'], callback=extract_likes, meta=dict({'likes_from': 'album.comment'}, **response.meta))


def extract_albums_data(response):
    def extract_albums(res):
        albums = res.body.xpath('//span/a')
        for album in albums:
            print(f'++ Found album {album.text}')
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
