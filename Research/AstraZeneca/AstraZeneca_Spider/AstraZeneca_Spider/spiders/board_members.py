import scrapy
from ..items import AstrazenecaSpiderItem

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
        page = response.url.split("/")[-2]
        board_members = response.css('h2.bio__header')
        print('===========================================================================================================================================')
        for board_member in board_members:
            name, title = board_member.css('span::text').getall()

            items = AstrazenecaSpiderItem()
            items['name'] = name
            items['title'] = title

            yield items
        #filename = f'board_members-{page}.html'
        #with open(filename, 'wb') as f:
        #    f.write(board_members)
        #self.log(f'Saved file {filename}')

        #filename = f'board_members-{page}.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log(f'Saved file {filename}')