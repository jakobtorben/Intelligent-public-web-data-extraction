# command to run is: scrapy crawl extract_board -o HSBC_board.csv

# imports
import scrapy
from items import HsbcItem

class extract_board(scrapy.Spider):
    name = 'extract_board'
    # define URLs
    allowed_domains = ['www.hsbc.com/who-we-are/leadership/']
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
            items = HsbcItem()

            # asign fiealds
            items['name'] = name
            items['title'] = title

            # return items
            yield items
