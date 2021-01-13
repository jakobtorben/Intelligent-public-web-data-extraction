# command to run is: scrapy crawl Unilever_board -o Unilever_board.csv

# imports
import scrapy
from ManWebScraper.items import Board
import datetime

class Unilever_board(scrapy.Spider):
    name = 'Unilever_board'

    # define URLs
    allowed_domains = ['www.unilever.com/']

    # define URLs and parsing method
    def start_requests(self):
        # current site
        yield scrapy.Request('http://www.unilever.com/about/who-we-are/our-leadership/', self.parse_current)

        # archived sites
        yield scrapy.Request('http://web.archive.org/web/20150801233936/http://www.unilever.com/about/who-we-are/our-leadership/', self.parse_2015_2020)
        yield scrapy.Request('https://web.archive.org/web/20130218181609/http://www.unilever.com/aboutus/companystructure/unileverexecutive/index.aspx', self.parse_2013_2015)

    
    def create_board(self, name, title, year):

        # create item for export
        item = Board()

        # asign fields
        item['company'] = 'Unilever'
        item['title'] = title
        item['year'] = year
        item['name'] = name

        yield item


    # parse the current Unilever board
    def parse_current(self, response):

        # define selector that contains all items
        all_people = response.css("article")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("div>h3>a").attrib['title']
            # manually parse title
            title = person.css("div>h3>a::text").get()

            now = datetime.datetime.now()
            year = now.year

            # Return item
            yield self.create_board(name, title, year)


    # parse the board from 2015-2020
    def parse_2015_2020(self, response):

        # define selector that contains all items
        all_people = response.css("article")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("div>h3>a").attrib['title']
            # manually parse title
            title = person.css("div>h3>a::text").get()

            # find the year from the crawled URL
            url = response.request.url
            date_info = url.split("/")[4]
            year = date_info[:4]

            # Return item
            yield self.create_board(name, title, year)


    # parse the board from 2013-2015
    def parse_2013_2015(self, response):

        # define selector that contains all items
        all_people = response.css("section>aside")

        # iterate through items
        for person in all_people:
            raw = person.css("div>div>p:nth-child(3)>a::text").extract()[0]
            info = raw.split(' – ')
            # Different types of - have been used
            if len(info) == 1:
                info = raw.split(' - ')
            name, title = info
            # Clean up typo on webpage
            if ';' in title:
                title = title.replace(';', '')

            # find the year from the crawled URL
            url = response.request.url
            date_info = url.split("/")[4]
            year = date_info[:4]

            # Return item
            yield self.create_board(name, title, year)
