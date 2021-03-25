import scrapy
import random
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


    """
    Find all the links on a page, choose one at random, follow that link and repeat.
    This function is recursive and untested.


    def parse_next_page(self, response):
        # get all the links
        for sel in response.xpath('//ul/li'):
            item = ScrapyNavigatorItem()
            # save the link
            item['link'] = sel.xpath('a/@href').extract()
            yield item

        # list of all possible next pages
        next_page = response.css("a::attr('href')")

        # if there is a valid next page
        if next_page:
            # choose new page at random
            selection = random.randint(0,len(next_page))
            url = response.urljoin(next_page[selection].extract())
            # use this function to parse it recursively
            yield scrapy.Request(url, self.parse_next_page)

    """