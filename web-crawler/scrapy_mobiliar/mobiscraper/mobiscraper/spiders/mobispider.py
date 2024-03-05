import scrapy
from mobiscraper.items import MobiItem


def get_joined_text(list_of_text_elements):
    import re

    pattern = re.compile(r"^\s*$")
    return "".join(
        [
            item.strip() + " "
            for item in list_of_text_elements.extract()
            if not pattern.match(item)
        ]
    )


# class MobispiderSpider(scrapy.Spider):
#     name = "mobispider"
#     allowed_domains = ["mobiliar.ch"]
#     start_urls = [
#         "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/privat-rechtsschutz"
#         # "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/schaeden-an-ihrer-mietwohnung"
#         # "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/wertsachenversicherung"
#         # "https://www.mobiliar.ch/hub/wohnen/umbau"
#     ]

#     # custom_settings = {"FEEDS": {"test.json": {"format": "json", "overwrite": True}}}

#     def parse(self, response):
#         article = response.css("article.node")
#         entire_text = article.css("div")
#         summary_box = article.css("div.paragraphs-items--pg-advanced-textbox *::text")
#         if len(summary_box) == 0:
#             summary_box = article.css("div.node-field--name-field-pp-summary *::text")

#         summary_box_txt = get_joined_text(summary_box)
#         accordion = article.css(
#             "div.paragraphs-items--faq.paragraphs-items-full.paragraphs-paragraphs-items--faq-full *::text"
#         )
#         accordion_txt = get_joined_text(accordion)
#         txt_a = article.css("div.node-field--name-field-cbpb-txt *::text")
#         txt_b = article.css("div.node-field--name-field-gb-body *::text")
#         txt_c = article.css("div.node-field--type-text-with-summary *::text")
#         txt_d = article.css("div.node-field--name-field-page-body *::text")
#         if len(txt_a) > 0:
#             texts = get_joined_text(txt_a)
#         elif len(txt_b) > 0:
#             texts = get_joined_text(txt_b)
#         elif len(txt_c) > 0:
#             texts = get_joined_text(txt_c)
#         elif len(txt_d) > 0:
#             texts = get_joined_text(txt_d)
#         else:
#             texts = ""

#         mobi_item = MobiItem()

#         mobi_item["url"] = response.url
#         mobi_item["page_title"] = article.css("h1#page-title span::text").get()
#         mobi_item["sub_title"] = entire_text.css("h2 div::text").get()
#         mobi_item["introduction"] = entire_text.css(
#             "div.node-field--name-field-shared-lead-text p::text"
#         ).get()
#         mobi_item["summary_box"] = summary_box_txt
#         mobi_item["content"] = texts
#         mobi_item["accordion"] = accordion_txt

#         yield mobi_item


# def parse(self, response):
#     links = response.css("a::attr(href)").extract()

#     for link in links:
#         if link.startswith(
#             "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/"
#         ):
#             yield {"url": link}
#         else:
#             pass


#   fetch("https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/so-finanzieren-sie-ihr-neues-zuhause")


# import scrapy

# class MobispiderSpider(scrapy.Spider):
#     name = "mobispider"
#     allowed_domains = ["mobiliar.ch"]
#     start_urls = [
#         "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/"
#         # "https://www.mobiliar.ch/versicherungen-und-vorsorge/services/praemienrechner"
#     ]

#     def parse(self, response):
#         links = response.css("a::attr(href)").extract()

#         for link in links:
#             if link.startswith(
#                 "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/"
#             ):
#                 yield {"url": link}
#             else:
#                 pass


# https://www.youtube.com/watch?v=o1g8prnkuiQ

# import scrapy
# from bs4 import BeautifulSoup
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor


# class MobispiderSpider(CrawlSpider):
#     name = "mobispider"
#     allowed_domains = ["mobiliar.ch"]

# start_urls = [
#     "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/"
# ]
# rules = (
#     Rule(LinkExtractor(allow="ratgeber"), callback="parse_item"),
# )

# def parse_item(self, response):

# This code extracted the whole html inside the block-mainpagecontent
# current_url = response.url
# if current_url.endswith("/"):
#     page_name = current_url.split("/")[-2]
# else:
#     page_name = current_url.split("/")[-1]

# html_content = response.css("div#block-mainpagecontent").extract_first()
# soup = BeautifulSoup(html_content)  # , "html.parser"

# yield {
#     f"{page_name}": soup.get_text().strip(),
# }


""" This follwing parser is perfect to parse all ratgeber pages """

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class MobispiderSpider(CrawlSpider):
    name = "mobispider"
    allowed_domains = ["mobiliar.ch"]
    start_urls = [
        # "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/"
        "https://www.mobiliar.ch"
    ]

    rules = (
        Rule(
            LinkExtractor(
                # allow="https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/"
                # allow="https://www.mobiliar.ch/versicherungen-und-vorsorge/fahrzeuge-und-reisen/ratgeber/"
                # allow="ratgeber"  # to scrape all ratgeber pages
                allow=()  # to scrape all pages of Mobiliar
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        article = response.css("article.node")
        entire_text = article.css("div")
        summary_box = article.css("div.paragraphs-items--pg-advanced-textbox *::text")
        if len(summary_box) == 0:
            summary_box = article.css("div.node-field--name-field-pp-summary *::text")

        summary_box_txt = get_joined_text(summary_box)
        accordion = article.css(
            "div.paragraphs-items--faq.paragraphs-items-full.paragraphs-paragraphs-items--faq-full *::text"
        )
        accordion_txt = get_joined_text(accordion)
        txt_a = article.css("div.node-field--name-field-cbpb-txt *::text")
        txt_b = article.css("div.node-field--name-field-gb-body *::text")
        txt_c = article.css("div.node-field--type-text-with-summary *::text")
        txt_d = article.css("div.node-field--name-field-page-body *::text")
        if len(txt_a) > 0:
            texts = get_joined_text(txt_a)
        elif len(txt_b) > 0:
            texts = get_joined_text(txt_b)
        elif len(txt_c) > 0:
            texts = get_joined_text(txt_c)
        elif len(txt_d) > 0:
            texts = get_joined_text(txt_d)
        else:
            texts = ""

        mobi_item = MobiItem()

        mobi_item["url"] = response.url
        mobi_item["page_title"] = article.css("h1#page-title span::text").get()
        mobi_item["sub_title"] = entire_text.css("h2 div::text").get()
        mobi_item["introduction"] = entire_text.css(
            "div.node-field--name-field-shared-lead-text p::text"
        ).get()
        mobi_item["summary_box"] = summary_box_txt
        mobi_item["content"] = texts
        mobi_item["accordion"] = accordion_txt

        yield mobi_item
