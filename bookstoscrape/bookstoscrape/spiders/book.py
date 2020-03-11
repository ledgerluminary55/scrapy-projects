# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    #start_urls = ['http://books.toscrape.com']

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com', headers={
            'Uger-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3/a"),
             callback='parse_item', follow=True, process_request='set_user_agent'),

        Rule(LinkExtractor(
            restrict_xpaths="//li[@class='next']/a"), process_request='set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent

        return request

    def parse_item(self, response):
        yield {
            'url': response.url,
            'title': response.xpath(".//div[contains(@class, 'product_main')]/h1/text()").get(),
            'price': response.xpath(".//p[@class='price_color']/text()").get()
            # 'User-Agent': response.request.headers['User-Agent']
        }
