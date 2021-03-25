import scrapy
from ..items import ScrapyNavigatorItem

class HsbcSpider(scrapy.Spider):
    name = 'HSBC'
    allowed_domains = ['hsbc.com']
    start_urls = ['https://www.hsbc.com/who-we-are']

    # function that finds links on page and clicks them
    def parse(self, response):
        for href in response.css("a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)
    
    # function that deals with pages returned from above        
    def parse_dir_contents(self, response):
        item = ScrapyNavigatorItem()
        for sel in response.xpath('//ul/li'):
            item['link'] = sel.xpath('a/@href').extract()
            yield item
