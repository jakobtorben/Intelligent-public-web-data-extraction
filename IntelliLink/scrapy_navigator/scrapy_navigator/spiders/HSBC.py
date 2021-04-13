import scrapy
import random
from ..items import ScrapyNavigatorItem

class HsbcSpider(scrapy.Spider):
    name = 'HSBC'
    allowed_domains = ['hsbc.com']
    start_urls = ['https://www.hsbc.com/who-we-are']
    
    def __init__(self):
        self.global_list = []
        self.ignore_status = ['403', '404']
        self.max_requests = 1000
        self.count = 0

    def start_requests(self):
        yield scrapy.Request('https://www.hsbc.com/who-we-are', callback = self.parse)

    # function that finds links on page and clicks them
    def parse(self, response):
        pageurl = []
        for href in response.css("a::attr('href')"):
            url = response.urljoin(href.extract())
            if url in self.global_list:
                continue
            if '#' in url:
                continue
            if "javascript:void(0)" in url:
                continue
            if "mailto" in url:
                continue
            if scrapy.http.Response(url).status in self.ignore_status:
                continue
            pageurl.append(url)
            yield scrapy.Request(url, callback = self.parse_attr)

        new_urls = self.page_agent(pageurl, 2)
        for new_url in new_urls:
            if (self.count < self.max_requests):
                yield scrapy.Request(new_url, callback = self.parse)


    def parse_attr(self, response):
        item = ScrapyNavigatorItem()
        item['link'] = response.url
        item['relevance'] = self.relevance(response.url)
        self.count += 1
        return item

    
    def page_agent(self, pageurl, size):
        new_urls = []
        for url in range(size):
            valid = False
            while (valid == False):
                selection = random.randint(0, len(pageurl)-1)
                if pageurl[selection] not in new_urls:
                    valid = True
                elif scrapy.response(pageurl[selection]).status in self.ignore_status:
                    valid = False
                    
            new_urls.append(pageurl[selection])
        return new_urls


    def relevance(self, link):
        return 1

    """
    
    # function that deals with pages returned from above        
    def parse_dir_contents(self, response):
        item = ScrapyNavigatorItem()
        for sel in response.xpath('//ul/li'):
            item['link'] = sel.xpath('a/@href').extract()
            print("link ", item['link'])
            item['relevance'] = self.relevance(item['link'])
            yield item
    """
    



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
