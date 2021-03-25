# command to run is: scrapy crawl GSK_board -o GSK_board.csv


"""

Manual parsing of gsk.com & archived versions of gsk.com from web.archive.org

Issues:

- Historical data extraction completely dependent on web.archive.org, if URLs change the whole extraction will break
- New parser has to be defined every time website html changes
- Extraction is manual, html has to be inspected to define parse function

"""

# imports
import scrapy
from ..items import Board
import datetime

class GSK_board(scrapy.Spider):
    name = 'GSK_board'

    # define URLs
    allowed_domains = ['www.gsk.com/']

    # define URLs and parsing method
    def start_requests(self):
        # current site
        yield scrapy.Request('https://www.gsk.com/en-gb/about-us/corporate-executive-team/',self.parse_current)

        # archived sites
        yield scrapy.Request('https://web.archive.org/web/20161120073949/http://www.gsk.com/en-gb/about-us/corporate-executive-team',self.parse_2016_current)
        yield scrapy.Request('https://web.archive.org/web/20140703075605/http://www.gsk.com/about-us/corporate-executive-team.html',self.parse_2014_2016)



    def create_board(self, name, title, year):

        # create item for export
        item = Board()

        # asign fields
        item['company'] = 'GSK'
        item['title'] = title
        item['year'] = year
        item['name'] = name
        
        return item

    # parse the current GSK board
    def parse_current(self, response):
        # define selector that contains all items
        all_people = response.css("li.grid-listing__item")
        print(all_people)
        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("a>div>h2::text").get()
            # manually parse title
            title = person.css("a>div>p::text").get()

            now = datetime.datetime.now()
            year = now.year

            # Return item
            yield self.create_board(name,title,year)

    # parse the board from 2015-2018
    def parse_2016_current(self, response):
        # define selector that contains all items
        all_people = response.css("article.listing-item.with-image")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("h3>a::text").get()
            # manually parse title
            title = person.css("p::text").get()

            # find the year from the crawled URL
            url = response.request.url
            date_info = url.split("/")[4]
            year = date_info[:4]

            # Return item
            yield self.create_board(name,title,year)

    # parse the board from 2013-2014
    def parse_2014_2016(self, response):
        # define selector that contains all items
        all_people = response.css("a.titleLink.textDecorateNone")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("h2>span.textDecorateNone::text").getall()[0]
            print(name)
            # manually parse title
            title = person.css("h2>span.textDecorateNone::text").getall()[1]

            # find the year from the crawled URL
            url = response.request.url
            date_info = url.split("/")[4]
            year = date_info[:4]

            # Return item
            yield self.create_board(name,title,year)
