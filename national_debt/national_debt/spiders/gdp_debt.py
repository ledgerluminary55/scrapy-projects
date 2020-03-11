# -*- coding: utf-8 -*-
import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['www.worldpopulationreview.com']
    start_urls = [
        'http://www.worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath("//table[@class='table table-striped']/tbody/tr")

        for row in rows:
            country_name = row.xpath(".//td[1]/a/text()").get()
            gdp_debt = row.xpath(".//td[2]/text()").get()
            population = row.xpath(".//td[3]/text()").get()

            yield {
                'country_name': country_name,
                'gdp_debt': gdp_debt,
                'population': population
            }