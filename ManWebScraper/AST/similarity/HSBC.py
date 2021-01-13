# command to run is: scrapy crawl HSBC_board -o HSBC_board.csv


"""

Manual parsing of HSBC.com & archived versions of HSBC.com from web.archive.org

Issues:

- Historical data extraction completely dependent on web.archive.org, if URLs change the whole extraction will break
- New parser has to be defined every time website html changes
- Extraction is manual, html has to be inspected to define parse function

"""

# imports
import scrapy
from ManWebScraper.items import Board
import datetime

class HSBC_board(scrapy.Spider):
    name = 'HSBC_board'

    # define URLs
    allowed_domains = ['www.hsbc.com/']

    # define URLs and parsing method
    def start_requests(self):
        # current site
        yield scrapy.Request('http://hsbc.com/who-we-are/leadership/',self.parse_current)

        # archived sites
        yield scrapy.Request('http://web.archive.org/web/20181109052314/https://www.hsbc.com/about-hsbc/leadership', self.parse_2015_2018)
        yield scrapy.Request('http://web.archive.org/web/20171109052314/https://www.hsbc.com/about-hsbc/leadership', self.parse_2015_2018)
        yield scrapy.Request('http://web.archive.org/web/20161109052314/https://www.hsbc.com/about-hsbc/leadership', self.parse_2015_2018)
        yield scrapy.Request('http://web.archive.org/web/20151109052314/https://www.hsbc.com/about-hsbc/leadership', self.parse_2015_2018)
        yield scrapy.Request('https://web.archive.org/web/20141202033024/http://www.hsbc.com/about-hsbc/leadership', self.parse_2013_2014)
        yield scrapy.Request('https://web.archive.org/web/20131121204902/http://www.hsbc.com/about-hsbc/leadership', self.parse_2013_2014)

    def create_board(self, name, title, year):

        # create item for export
        item = Board()

        # asign fields
        item['company'] = 'HSBC'
        item['title'] = title
        item['year'] = year
        item['name'] = name

        yield item

    # parse the current HSBC board
    def parse_current(self, response):
        # define selector that contains all items
        all_people = response.css("li.directors-index__item")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("a>div>div>h3.contact-large-image-teaser__header::text").get()
            # manually parse title
            title = person.css("a>div>div>p>span::text").get()

            now = datetime.datetime.now()
            year = now.year

            # Return item
            yield self.create_board(name,title,year)

    # parse the board from 2015-2018
    def parse_2015_2018(self, response):
        # define selector that contains all items
        all_people = response.css("li.profile-col1")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("div>h3>a.title-profile.text-red::text").get()
            # manually parse title
            title = person.css("div>p.profile-info::text").get()

            # find the year from the crawled URL
            url = response.request.url
            date_info = url.split("/")[4]
            year = date_info[:4]

            # Return item
            yield self.create_board(name,title,year)

    # parse the board from 2013-2014
    def parse_2013_2014(self, response):
        # define selector that contains all items
        all_people = response.css("div.profile-col1")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("div>a.title-profile.text-red::text").get()
            # manually parse title
            title = person.css("div>p.profile-info.profile-desg.bold::text").get()

            # find the year from the crawled URL
            url = response.request.url
            date_info = url.split("/")[4]
            year = date_info[:4]

            # Return item
            yield self.create_board(name,title,year)
