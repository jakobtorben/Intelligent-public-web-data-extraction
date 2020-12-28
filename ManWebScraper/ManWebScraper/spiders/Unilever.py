# command to run is: scrapy crawl Unilever_board -o Unilever_board.csv

# imports
import scrapy
from ManWebScraper.items import Board
import datetime

class Unilever_board(scrapy.Spider):
    name = 'Unilever_board'

    # define URLs
    allowed_domains = ['www.unilever.com/']
    start_urls = ['http://www.unilever.com/about/who-we-are/our-leadership/',
                  'http://web.archive.org/web/20150801233936/http://www.unilever.com/about/who-we-are/our-leadership/',
                  'https://web.archive.org/web/20130218181609/http://www.unilever.com/aboutus/companystructure/unileverexecutive/index.aspx']

    def parse(self, response):
        # Extract date
        if 'web.archive.org' in response.url:
            datestr = response.xpath('//*[@id="wmtb"]/input[3]').attrib['value']
            date = datetime.datetime.strptime(datestr, '%Y%m%d%H%M%S').date()
        else:
            date = datetime.date.today()

        if date.year >= 2015:
            all_people = response.css("article")
        else:
            all_people = response.css("section>aside")

        # iterate through people and parse for items
        for person in all_people:
            if date.year >= 2015:
                name = person.css("div>h3>a").attrib['title']
                title = person.css("div>h3>a::text").get()
            else:
                raw = person.css("div>div>p:nth-child(3)>a::text").extract()[0]
                info = raw.split(' – ')
                # Different types of - have been used
                if len(info) == 1:
                    info = raw.split(' - ')
                name, title = info
                # Clean up typo on webpage
                print(title) 
                if ';' in title:
                    title = title.replace(';', '')

            # create item for export
            item = Board()
            item['company'] = 'Unilever'
            item['title'] = title
            item['date'] = date
            item['name'] = name

            # return item
            yield item
