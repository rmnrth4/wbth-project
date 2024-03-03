# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MobiscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MobiItem(scrapy.Item):
    url = scrapy.Field()
    page_title = scrapy.Field()
    sub_title = scrapy.Field()
    introduction = scrapy.Field()
    summary_box = scrapy.Field()
    content = scrapy.Field()
    accordion = scrapy.Field()
