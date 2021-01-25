# Manual parsing of shell.com & archived versions of shell.com from web.archive.org
# command to run is: scrapy crawl Shell_board -o Shell_board.csv

# imports
import scrapy
from ..items import Board
import datetime


class Shell_board(scrapy.Spider):
    name = 'Shell_board'

    # define URLs
    allowed_domains = ['www.shell.com/']

    # define URLs and parsing method
    def start_requests(self):
        # current site
        yield scrapy.Request('https://www.shell.com/about-us/leadership/executive-committee.html/', self.parse_current)

        # archived sites
        yield scrapy.Request('https://web.archive.org/web/20170617034334/https://www.shell.com/about-us/leadership/executive-committee.html', self.parse_2015_current)
        yield scrapy.Request('https://web.archive.org/web/20131211150816/http://www.shell.com/global/aboutshell/who-we-are/leadership/executive-committee.html', self.parse_2013_2015)

    def create_board(self, name, title, year):

        # create item for export
        item = Board()

        # asign fields
        item['company'] = 'Shell'
        item['title'] = title
        item['year'] = year
        item['name'] = name

        return item

    # parse the current HSBC board
    def parse_current(self, response):
        # define selector that contains all items
        all_people = response.css("div.component.component--fat.promo-list.promo-list--tiles.promo-list--4-or-more-items.promo-list--palette-0").css("div.promo-list__text")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("h3>a>span::text").get()

            # manually parse title
            title = person.css("p::text").get()

            now = datetime.datetime.now()
            year = now.year

            # Return item
            yield self.create_board(name, title, year)

    # parse the board from 2015-2018
    def parse_2015_current(self, response):
        # define selector that contains all items
        all_people = response.css("section.component.promo-list.promo-list--tiles.promo-list--4-or-more-items.colour--palette-0").css("article.promo-list__item")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("h3>a>span::text").get()

            # manually parse title
            title = person.css("p::text").get()
            # extract title from text body
            title = title.replace(name+" is ", '')

            # find the year from the crawled URL
            url = response.request.url
            date_info = url.split("/")[4]
            year = date_info[:4]

            # Return item
            yield self.create_board(name, title, year)

    # parse the board from 2013-2014
    def parse_2013_2015(self, response):
        # define selector that contains all items
        all_people = response.css("div.directorylist.parbase.basecomponent")

        # iterate through items
        for person in all_people:
            # manually parse name

            name = person.css("div>div>div.text>h3>a::text").get()
            # Remove trailing \n and \t
            name = name.strip("\n\t")

            # manually parse title
            title = person.css("div>div>div.text>p::text").get()
            title = title.strip("\n\t")

            # find the year from the crawled URL
            url = response.request.url
            date_info = url.split("/")[4]
            year = date_info[:4]

            # Return item
            yield self.create_board(name, title, year)
