# -*- coding: utf-8 -*-
import scrapy


class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['www.geekbuying.com']
    #start_urls = ['https://www.geekbuying.com/deals']

    def start_requests(self):

        yield scrapy.Request(url="https://www.geekbuying.com/deals", callback=self.parse, headers={'Uger-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'})

    def parse(self, response):
        products = response.xpath("//div[@class='category_li']")

        for product in products:

            product_name = product.xpath(
                ".//a[@class='category_li_link']/text()").get()
            product_link = product.xpath(
                ".//a[@class='category_li_link']/@href").get()
            product_price = product.xpath(
                ".//div[@class='category_li_price']/span/text()").get()
            promotion_ends = product.xpath(
                ".//div[@class='category_li_claibg']/span/text()").get()

            yield {
                'product_name': product_name,
                'product_link': product_link,
                'product_price': product_price,
                'promotion_ends': promotion_ends
            }

        next_page = response.xpath("//a[@class='next']/@href").get()

        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
        
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse, headers={
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        #     })
