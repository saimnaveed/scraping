import scrapy

file=open("test.txt","w+")
class PhonePriceSpider(scrapy.Spider):
    name = 'phone_price'
    base_url_template = 'https://www.daraz.pk/smartphones/?page={}'
    start_urls = [base_url_template.format(1)]
    def parse(self, response):
        phone_urls=response.xpath('/html/body/main/section[2]/section[2]/div/a/@href').extract()
        for phone_url in phone_urls:
            file.write(str(phone_url)+":")
            yield scrapy.Request(url=phone_url,callback=self.parse_details)
        if response.xpath('/a[@title="next"]'):
            num=(response.css('html body.l-full-hd.ui-page-bg.thm-core.thm-spinbasket.thm-local.thm-oshun.-vertical-fashion.-has-sidebar.dir-ltr main.osh-container section.osh-content section.osh-filters.-horizontal.-fashion div.osh-row.bottom div.-pull-left ul.osh-pagination.-horizontal li.item.-selected a::attr(title)').extract()[0])
            yield scrapy.Request(self.base_url_template.format(num+1))
    def parse_details(self,response):
        result= response.xpath('/html/body/main/section[@class="sku-detail"]/div[@class="details-wrapper"]/div[@class="details -validate-size"]/div[@class="details-footer"]/div[@class="price-box"]/div/span[@class="price"]/span[@dir="ltr"]/text()').extract()
        file.write(str(result)+",")
        yield {"price":result}
    file.close()
