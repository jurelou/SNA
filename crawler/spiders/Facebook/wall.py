# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------

from crawler.http import Request
from crawler.utils import open_page
from crawler.core import Outcome


def extract_likes(response):
    select_all = response.body.xpath('//tbody/tr/td/div/div/a')[0]

    def extract(res):
        next_page = res.body.xpath("//li/table/tbody/tr/td/div/a")
        likes = res.body.xpath("//td/div/h3/a")
        if likes:
            for like in likes:
                # print("\t->", like.text, like.attrib['href'])
                # TODO: store result
                pass
        if next_page:
            yield Request("https://mbasic.facebook.com/" + next_page[0].attrib['href'], callback=extract, meta=res.meta)
    yield Request("https://mbasic.facebook.com/" + select_all.attrib['href'], callback=extract, meta=response.meta)


def extract_post_data(response):
    likes = response.body.xpath('//div[@id="root"]/div/div/div/div/a')
    comments_author = response.body.xpath('//div/div/div/h3/a')
    comments_likes = response.body.xpath(
        "//div/span/span/a[not(text()='React') and not(text()='Like')]")
    if likes:
        yield Request("https://mbasic.facebook.com/" + likes[0].attrib['href'], callback=extract_likes, meta=dict({'likes_from': 'wall.post'}, **response.meta))
    if comments_author and comments_likes:
        for author in comments_author:
            # TODO: store result
            #print("AUTHOR ->", author.text, author.attrib['href'])
            pass
        for comment_like in comments_likes:
            yield Request("https://mbasic.facebook.com/" + comment_like.attrib['href'], callback=extract_likes, meta=dict({'likes_from': 'wall.post.comment'}, **response.meta))


# Limit the number of wall pages to recover
limit = 1


def extract_posts_data(response):
    global limit
    limit -= 1
    next_page = response.body.xpath("//a[span[text()='See more stories']]")
    posts = response.body.xpath(
        "//div/div/div/span[starts-with(@id, 'like')]/a[not(text()='React') and not(text()='Like')]")
    if posts:
        for post in posts:
            yield Request("https://mbasic.facebook.com/" + post.attrib['href'], callback=extract_post_data, meta=response.meta)
    if next_page and limit > 0:
        yield Request("https://mbasic.facebook.com/" + next_page[0].attrib['href'], callback=extract_posts_data, meta=response.meta)
