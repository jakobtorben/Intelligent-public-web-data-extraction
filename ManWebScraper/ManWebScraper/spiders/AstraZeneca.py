import scrapy
from ManWebScraper.items import Board
import re
from scrapy.spiders import XMLFeedSpider
from scrapy.http import HtmlResponse
from scrapy.http import Response
from scrapy.selector import Selector

"""
To run this, simply use 'scrapy crawl AstraZeneca_board'
"""

class AstraZeneca_board(scrapy.Spider): # online solutions suggest that reading XML is best when you inherit XML class

    """
    Instantiates a 'spider' that can crawl the web.
    """
    name = 'AstraZeneca_board'

    allowed_domains = ['www.astrazeneca.com/']
    start_urls = [
        'https://www.astrazeneca.com/our-company/leadership.html'
    ]



    def start_requests(self):
        """
        This method seems to be native to scrapy --> it allows you to set up a start sequence!
        If unspecified, I believe scrapy will look for 'parse' method
        """
        yield scrapy.Request('https://www.astrazeneca.com/sitemap.xml', self.parse_XML)
        yield scrapy.Request('https://www.astrazeneca.com/our-company/leadership.html',self.parse)

    def parse_XML(self, response):
        page = Selector(response) # this is useless, for some reason can't read the Xpath??
        text = response.text
        print(text)

        text = text.replace("\n", "")
        text = re.sub(' +', '', text)  # reduce multispacing to single spacing
        print(re.findall(r'<url><loc>https://www.astrazeneca.com/our-company/leadership.html(.*?)</url>', text))

        yield response

    def parse(self, response):

        all_people = response.css('h2.bio__header')

        for person in all_people:
            name, title = person.css('span::text').getall()
            item = Board()
            item['company'] = 'AstraZeneca'
            item['name'] = name
            item['title'] = title[1:-1]
            print(name, title)
            yield item


"""
Useful links:
https://www.youtube.com/watch?v=ALizgnSFTwQ

"""