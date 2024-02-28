# https://blog.logrocket.com/build-python-web-crawler/

import requests
from lxml import html
from items import StoreItem
import response

item1 = StoreItem("Lenovo IdeaPad", 749, "Walmart")


# def get_source(page_url):
#     """
#     A function to download the page source of the given URL.
#     """
#     r = requests.get(page_url)
#     return html.fromstring(r.content)


# HOME_PAGE = "http://books.toscrape.com/index.html"
# source = get_source(HOME_PAGE)


# li_xpath = "//li[contains(@class, 'col-xs-6')]"
# names_xpath = ".//h3[@class='product_pod']/text()"
# price_xpath = ".//p[@class'price_color']/text()"
# availability_xpath = ".//p[@class'instock availability']/text()"

# li_list = source.xpath(li_xpath)
# items = list()
# for li in li_list:
#     name = li.xpath(names_xpath)
#     price = li.xpath(price_xpath)
#     availability = li.xpath(availability_xpath)

#     # Store inside a class
#     item = StoreItem(name, price, availability)
#     items.append(item)
# print(len(items))

# # r = requests.get("http://books.toscrape.com/index.html")
# # source = html.fromstring(r.content)
# # li_list = source.xpath(li_xpath)
# # print(li_list[1]names_xpath)


def get_source(page_url):
    """
    A function to download the page source of the given URL.
    """
    r = page_url
    return html.fromstring(r.content)
