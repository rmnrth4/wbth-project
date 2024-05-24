import scrapy
from mobiscraper.items import MobiItem
from scrapy.linkextractors import LinkExtractor


def get_joined_text(list_of_text_elements):
    import re

    pattern = re.compile(r"^\s*$")
    joined_text = ""
    for item in list_of_text_elements.extract():
        if not pattern.match(item):
            joined_text += item.strip() + " "
    return joined_text.rstrip()


def avoid_none_result(css_selector_statement):
    if css_selector_statement is None:
        return ""
    else:
        return css_selector_statement


""" This follwing parser is perfect to parse all pages """

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
                # allow="https://www.mobiliar.ch/die-mobiliar/medien/medienmitteilungen/"
                # allow="https://www.mobiliar.ch/versicherungen-und-vorsorge/fahrzeuge-und-reisen/ratgeber/"
                # allow="ratgeber"  # to scrape all ratgeber pages
                allow=(),
                deny=[
                    "kunst.mobiliar.ch",
                    "report.mobiliar.ch",
                    "mobiliare.ch",
                    "mobiliere.ch",
                    "jobs",
                    "generalagenturen",
                    "gallerySlide",
                    "vcard",
                ],  # to scrape all pages of Mobiliar
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        article = response.css("article.node")
        entire_text = article.css("div")
        summarybox = article.css("div.paragraphs-items--pg-advanced-textbox *::text")
        if len(summarybox) == 0:
            summarybox = article.css("div.node-field--name-field-pp-summary *::text")
        summarybox_txt = get_joined_text(summarybox)
        accordion = article.css(
            "div.paragraphs-items--faq.paragraphs-items-full.paragraphs-paragraphs-items--faq-full *::text"
        )
        accordion_txt = get_joined_text(accordion)
        grid_content = response.css("div#content.column div.grid").extract()
        maintext = article.css("div.node-field--type-text-long *::text")
        if len(maintext) > 0:
            txt = get_joined_text(maintext)
        else:
            txt = ""

        link_extractor = LinkExtractor()
        links_list = []
        for content in grid_content:
            links = link_extractor.extract_links(response.replace(body=content))
            for link in links:
                if link.url not in links_list:
                    links_list.append(link.url)

        mobi_item = MobiItem()

        mobi_item["url"] = response.url
        mobi_item["pagetitle"] = avoid_none_result(
            article.css("h1#page-title span::text").get()
        ).rstrip()
        mobi_item["subtitle"] = avoid_none_result(
            entire_text.css("h2 div::text").get()
        ).rstrip()
        mobi_item["introduction"] = avoid_none_result(
            entire_text.css("div.node-field--name-field-shared-lead-text p::text").get()
        ).rstrip()
        mobi_item["summarybox"] = summarybox_txt
        mobi_item["content"] = txt
        mobi_item["accordion"] = accordion_txt
        mobi_item["linkedpages"] = links_list

        yield mobi_item
