import scrapy
from ..items import AstrazenecaSpiderItem
import csv

class board_members(scrapy.Spider):
    """
    Instantiates a 'spider' that can crawl the web.
    """
    name = 'board_members'

    def start_requests(self):
        urls = [
            'https://www.astrazeneca.com/our-company/leadership.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('NEW PARSER')
        print('=============================================================================================')
        page = response.url.split("/")[-2]
        board_members = response.css('h2.bio__header')
        with open('data.csv', 'w') as f:
            # TODO fix repetition of names
            for board_member in board_members:
                name, title = board_member.css('span::text').getall()

                f.write('{},{}\n'.format(name, title[1:-1]))

        f.close()