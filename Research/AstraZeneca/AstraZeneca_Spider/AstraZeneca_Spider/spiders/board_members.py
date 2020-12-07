import scrapy

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
        filename = f'board_members-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')