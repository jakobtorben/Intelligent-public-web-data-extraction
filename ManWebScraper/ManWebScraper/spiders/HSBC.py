# command to run is: scrapy crawl extract_board -o HSBC_board.csv

# imports
import scrapy
from ManWebScraper.items import Board

class HSBC_board(scrapy.Spider):
    name = 'HSBC_board'

    # define URLs
    allowed_domains = ['www.hsbc.com/']
    start_urls = ['http://hsbc.com/who-we-are/leadership/']

    def parse(self, response):
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

            # asign fields
            item['company'] = 'HSBC'
            item['name'] = name
            item['title'] = title
            # Return item
            yield item
