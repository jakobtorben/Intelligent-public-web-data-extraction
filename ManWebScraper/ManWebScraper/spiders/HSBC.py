# command to run is: scrapy crawl HSBC_board -o HSBC_board.csv

# imports
import scrapy
from ManWebScraper.items import Board
import datetime

class HSBC_board(scrapy.Spider):
    name = 'HSBC_board'

    # define URLs
    allowed_domains = ['www.hsbc.com/']

    def start_requests(self):
        yield scrapy.Request('http://hsbc.com/who-we-are/leadership/',self.parse_current)
        yield scrapy.Request('http://web.archive.org/web/20181109052314/https://www.hsbc.com/about-hsbc/leadership', self.parse_2018)

    def parse_current(self, response):
        # define selector that contains all items
        all_people = response.css("li.directors-index__item")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("a>div>div>h3.contact-large-image-teaser__header::text").get()
            # manually parse title
            title = person.css("a>div>div>p>span::text").get()

            # create item for export
            item = Board()

            now = datetime.datetime.now()

            # asign fields
            item['company'] = 'HSBC'
            item['title'] = title
            item['year'] = now.year
            item['name'] = name

            # Return item
            yield item

    def parse_2018(self, response):
        # define selector that contains all items
        all_people = response.css("li.profile-col1")

        # iterate through items
        for person in all_people:
            # manually parse name
            name = person.css("div>h3>a.title-profile.text-red::text").get()
            # manually parse title
            title = person.css("div>p.profile-info::text").get()

            # create item for export
            item = Board()

            # asign fields
            item['company'] = 'HSBC'
            item['title'] = title
            item['year'] = 2018
            item['name'] = name

            # Return item
            yield item
