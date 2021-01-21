import scrapy
from ..items import Board
import re
from scrapy.spiders import XMLFeedSpider
from scrapy.http import HtmlResponse
from scrapy.http import Response
from scrapy.selector import Selector
from datetime import date

"""
To run this, simply use 'scrapy crawl Tesco_board'
Remember that you need to run this in the correct folder!
"""

class Tesco_board(scrapy.Spider):

    """
    Instantiates a 'spider' that can crawl the web.
    """
    name = 'Tesco_board'

    allowed_domains = ['www.tescoplc.com/']



    def start_requests(self):

        # current members
        yield scrapy.Request('https://www.tescoplc.com/about/board-board-committees-and-executive-committee/board/', self.parse_current)
        yield scrapy.Request('https://www.tescoplc.com/about/board-board-committees-and-executive-committee/executive-committee/', self.parse_current)

        # prior to 2012
        yield scrapy.Request('https://web.archive.org/web/20111001231324/http://www.tescoplc.com/about-tesco/board-and-management-team/', self.parse_prior_2012)

        # prior to 2011
        yield scrapy.Request('https://web.archive.org/web/20081113144316/http://www.tescoplc.com/plc/about_us/directors/', self.parse_prior_2011)

    def find_year(self, url):
        if 'web.archive' in url:
            year = url.split('https://web.archive.org/web/')[1][:4]
            return year
        else:
            return date.today().year


    def create_board(self, name, title, year):

        # create item for export
        item = Board()

        # assign fields
        item['company'] = self.name[:-6]
        item['title'] = title
        item['year'] = year
        item['name'] = name

        return item

    def parse_current(self, response):

        url = response.request.url

        all_people = response.css('div.people-profile__label')

        for person in all_people:
            name = person.css('strong::text').getall()[0]
            title = person.css('span::text').getall()[0]
            year = self.find_year(url)
            yield self.create_board(name,title,year)

    def parse_prior_2012(self, response):

        url = response.request.url

        all_people = response.css('#management').css('li')
        for person in all_people:
            name = person.css('h3::text').getall()[0]
            title = person.css('h4::text').getall()[0]
            year = self.find_year(url)
            yield self.create_board(name,title,year)

    def parse_prior_2011(self, response):

        url = response.request.url

        all_people = response.css('div.bod_bio')

        for person in all_people:
            name, title = person.css('span::text').getall()[0].split(',')[:2]
            year = self.find_year(url)
            yield self.create_board(name,title,year)


# NOTE: weirdly enough, there is now a data attribute in the CSV? Where is this from?