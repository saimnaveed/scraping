# -*- coding: utf-8 -*-
import scrapy
class MobilePricesSpider(scrapy.Spider):
    name = 'mobile_prices'
    allowed_domains = ['http:www.daraz.pk/phones-tablets/']
    start_urls = ['http://http:www.daraz.pk/phones-tablets//']

    def parse(self, response):
	 phone_urls = response.xpath('/html/body/main/section/div[2]/div/a/@href').extract()
        for phone_url in phone_urls:
            yield scrapy.Request(url=phone_url, callback=self.parse_details)

    def parse_details(self, response):
        result = response.xpath('/html/body/main/section[1]/div[2]/div/div[@class="details-footer"]/div[@class="price-box"]/div/span[@class="price"]/span[@dir="ltr"]/text()').extract()
        yield {"prices", result}
	
