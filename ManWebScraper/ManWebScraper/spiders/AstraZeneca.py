import scrapy
from ManWebScraper.items import Board


class AstraZeneca_board(scrapy.Spider):
    """
    Instantiates a 'spider' that can crawl the web.
    """
    name = 'AstraZeneca_board'

    allowed_domains = ['www.astrazeneca.com/']
    start_urls = [
        'https://www.astrazeneca.com/our-company/leadership.html'
    ]

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