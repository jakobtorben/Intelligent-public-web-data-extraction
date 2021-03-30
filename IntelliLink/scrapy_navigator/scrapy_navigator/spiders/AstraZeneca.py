import scrapy
import random
import re
from ..items import ScrapyNavigatorItem

def clean_html(text):
    #keep_letters = re.compile('[^a-zA-Z ]')

    # TODO refine these
    # removes html tags
    cleaner = re.compile('<.*?>')
    text = re.sub(cleaner, '', text)

    # removes \n characters that are actually str of \ + n
    text = re.sub(r'\\n', ' ', text)
    # removes html classes # TODO expand this to include other html attribs
    text = re.sub('class=', ' ', text)

    # removes any texts in brackets
    text = re.sub(r'\{.*?\}', ' ', text)
    text = re.sub(r'\[.*?\]', ' ', text)

    # removes commas
    text = re.sub(r',', ' ', text)

    # shrinks any whitespace to single whitespace
    text = re.sub(r"\s+", " ", text)

    #text = re.sub(keep_letters, '', text)

    #print(text)
    #text = re.sub(r'[\\\/\+\(\-\*\)]', ' ', text)
    #text =  re.sub(r"(?<!\_)[0-9]", '', text)
    return text


class AstraZenecaSpider(scrapy.Spider):
    name = 'AstraZeneca'
    # allowed_domains = ['wwAstraZeneca.com']
    start_urls = ['https://www.astrazeneca.com']

    # function that finds links on page and clicks them
    def parse(self, response):
        """ Creates start links for parse_dir_contents """

        for href in response.xpath("//a[not(contains(@href, '#'))]/@href"):
            # TODO make sure astrazeneca.com/ not duplicated?
            # TODO in general need to remove duplicates
            url = response.urljoin(href.extract())
            if url == 'https://www.astrazeneca.com/our-company.html':
                print(url)
                yield scrapy.Request(url, callback = self.parse_test)
            #reak


    def parse_test(self, response):
        item = response.body
        print(clean_html(str(item)))
                      #print(clean_html(item.extract_first()))

    # function that deals with pages returned from above
    def parse_dir_contents(self, response):
        item = ScrapyNavigatorItem()
        for sel in response.xpath('//ul/li'):
            # TODO @ricardo not sure what this is doing? is it doing parse again but at the
            # TODO link level as opposed to mainpage? Not convincedim
            print(sel)
            item['link'] = sel.xpath('a/@href').extract()
            print(item['link'])
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