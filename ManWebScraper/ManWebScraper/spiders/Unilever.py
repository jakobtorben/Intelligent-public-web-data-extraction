# command to run is: scrapy crawl Unilever_board -o Unilever_board.csv

# imports
import scrapy
from ManWebScraper.items import Board
import datetime

class Unilever_board(scrapy.Spider):
    name = 'Unilever_board'

    # define URLs
    allowed_domains = ['www.unilever.com/']
    start_urls = ['http://www.unilever.com/about/who-we-are/our-leadership/',
                  'http://web.archive.org/web/20150801233936/http://www.unilever.com/about/who-we-are/our-leadership/']

    def parse(self, response):
        # define selector that contains all items
        all_people = response.css("article")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("div>h3>a").attrib['title']

            # manually parse title
            title = person.css("div>h3>a::text").get()

            # create item for export
            item = Board()

            # asign fields
            item['company'] = 'Unilever'
            item['title'] = title
            item['year'] = year
            item['name'] = name


            # return items
            yield item
