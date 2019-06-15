# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# louis@jurczyk.fr wrote this code. As long as you retain this
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return. Louis Jurczyk
# ------------------------------------------------------------
import os
import random
import string
import webbrowser
from lxml import etree
from crawler.http import Response

def open_page(res):
    if not isinstance(res, Response):
    	raise ValueError(f'Inappropriate type {type(res)} for webbrowser.open_page, expected Response object')
    def random_string(size=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(size))
    file = "./temp/" + random_string() + ".html"
    if not os.path.exists("./temp"):
        os.mkdir("./temp")
    dom = etree.tostring(res.body, pretty_print=True, method="html")
    with open(file, "w+") as f: 
        f.write(str(dom, 'utf-8'))
    webbrowser.open_new_tab(os.getcwd() + "/" + file)