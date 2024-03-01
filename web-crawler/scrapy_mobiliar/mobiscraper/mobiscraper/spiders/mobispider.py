import scrapy
from bs4 import BeautifulSoup


class MobispiderSpider(scrapy.Spider):
    name = "mobispider"
    allowed_domains = ["mobiliar.ch"]
    start_urls = [
        "https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/so-finanzieren-sie-ihr-neues-zuhause"
    ]

    def parse(self, response):

        article = response.css("article.node")
        entire_text = article.css("div")
        paragraphs = entire_text.css(
            "div.node-field.node-field--name-field-pgp-paragraphs.node-field--type-entity-reference-revisions.node-field--label-hidden.node-field__items"
        )
        paragraph_sections = paragraphs.css("div.node-field__item *::text")

        texts = ""
        for item in paragraph_sections.extract():
            text = item.strip()
            if text:
                texts += text

        # print(texts)

        # html_content = response.css("div#block-mainpagecontent").extract_first()
        # soup = BeautifulSoup(html_content)

        yield {
            "page_title": article.css("h1#page-title span::text").get(),
            "sub_title": entire_text.css("h2 div::text").get(),
            "intro_text": entire_text.css(
                "div.node-field.node-field--name-field-shared-lead-text.node-field--type-text-long.node-field--label-hidden.node-field__item p::text"
            ).get(),
            "content": texts,
        }


#   fetch("https://www.mobiliar.ch/versicherungen-und-vorsorge/wohnen-und-eigentum/ratgeber/so-finanzieren-sie-ihr-neues-zuhause")


# sub_article_div = article.css("div")

# untertitel = h2_element = response.css('h2')
#             div_element = h2_element.css('div.node-field__item')
# abschnit_titel = response.css("div.node-field h2::text").get()
# ul_box = box.css("div.node-field ul")
# unordered_vorteile_list = ul_box.css("li::text")
# for ele in unordered_vorteile_list:

# nodes = response.css("div.node-field")

# h2_ele = nodes.css("h2::text")
# texts = nodes.css("p::text")

# node_field_items = response.css("div.node-field__item")
# for node in nodes:
#     yield {
#         # "h2_ele": response.css("div.node-field h2::text").get(),
#         "h2_ele": node.css("h2::text").get(),
#         "h4_ele": node.css("h4::text").get(),
#         # "text": response.css("div.node-field p::text").get(),
#         "text": node.css("p::text").get(),

#     }


# import scrapy

# from bs4 import BeautifulSoup
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor


# # https://www.youtube.com/watch?v=o1g8prnkuiQ
# class MobispiderSpider(CrawlSpider):
#     name = "mobispider"
#     allowed_domains = ["mobiliar.ch"]
#     start_urls = ["https://www.mobiliar.ch"]

#     rules = (
#         # Rule(LinkExtractor(allow="fahrzeuge-und-reisen")),
#         Rule(LinkExtractor(allow="versicherungen-und-vorsorge"), callback="parse_item"),
#     )

#     def parse_item(self, response):

#         # This code extracted the whole html inside the block-mainpagecontent
#         current_url = response.url
#         if current_url.endswith("/"):
#             page_name = current_url.split("/")[-2]
#         else:
#             page_name = current_url.split("/")[-1]

#         html_content = response.css("div#block-mainpagecontent").extract_first()
#         soup = BeautifulSoup(html_content)  # , "html.parser"

#         yield {
#             f"{page_name}": soup.get_text().strip(),
#         }
