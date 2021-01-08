import scrapy
from ManWebScraper.items import Board
import re
from scrapy.spiders import XMLFeedSpider
from scrapy.http import HtmlResponse
from scrapy.http import Response
from scrapy.selector import Selector
from datetime import date

"""
To run this, simply use 'scrapy crawl AstraZeneca_board'
Remember that you need to run this in the correct folder!
"""

class AstraZeneca_board(scrapy.Spider): # online solutions suggest that reading XML is best when you inherit XML class

    """
    Instantiates a 'spider' that can crawl the web.
    """
    name = 'AstraZeneca_board'

    allowed_domains = ['www.astrazeneca.com/']
    start_urls = [
        'https://www.astrazeneca.com/our-company/leadership.html'
    ]



    def start_requests(self):
        """
        This method seems to be native to scrapy --> it allows you to set up a start sequence!
        If unspecified, I believe scrapy will look for 'parse' method
        """
        #yield scrapy.Request('https://www.astrazeneca.com/sitemap.xml', self.parse_XML)


        #yield scrapy.Request('https://www.astrazeneca.com/our-company/leadership.html',self.parse_current)
        #yield scrapy.Request('https://web.archive.org/web/20160304110534/https://www.astrazeneca.com/our-company/leadership.html',self.parse_current)

        #yield scrapy.Request('https://web.archive.org/web/20151015023532/http://www.astrazeneca.com/About-Us/our-board-of-directors', self.parse_prior_2016)
        #yield scrapy.Request('https://web.archive.org/web/20151015023301/http://www.astrazeneca.com/About-Us/astrazeneca-senior-executive-team', self.parse_prior_2016)

        #yield scrapy.Request('https://web.archive.org/web/20120915030408/http://www.astrazeneca.com/About-Us/Board-and-management', self.parse_prior_2016)

        yield scrapy.Request('https://web.archive.org/web/20051028020248/http://www.astrazeneca.com/article/510901.aspx', self.parse_intermediate)
        #yield scrapy.Request('https://web.archive.org/web/20011212171535/http://www.astrazeneca.com/AboutUs/Board_and_management.htm', self.parse_prior_2002)


    def parse_XML(self, response):
        page = Selector(response) # this is useless, for some reason can't read the Xpath??
        text = response.text
        print(text)

        text = text.replace("\n", "")
        text = re.sub(' +', '', text)  # reduce multispacing to single spacing
        print(re.findall(r'<url><loc>https://www.astrazeneca.com/our-company/leadership.html(.*?)</url>', text))

        yield response

    def find_year(self, url):
        if 'web.archive' in url:
            year = url.split('https://web.archive.org/web/')[1][:4]
            return year
        else:
            return date.today().year

    def parse_current(self, response):

        url = response.request.url # this saves the url

        all_people = response.css('h2.bio__header')

        for person in all_people:
            name, title = person.css('span::text').getall()
            item = Board()
            item['company'] = 'AstraZeneca'
            item['name'] = name
            # strip necessary to remove white space and new line chars
            item['title'] = title[1:-1].strip(' ').strip('\n')
            item['year'] = self.find_year(url)
            print(name, title)
            yield item

    def parse_prior_2016(self, response):
        url = response.request.url
        all_people = response.css('dl')
        for person in all_people:
            name = person.css('dt::text').getall()
            title = person.css('dd.description::text').getall()[0]

            item = Board()
            item['company'] = 'AstraZeneca'
            item['name'] = name
            item['title'] = title
            item['year'] = self.find_year(url)
            yield item

    def parse_intermediate(self, response):
        url = response.request.url
        paragraphs = response.css('p')

        for p in paragraphs:
            name = p.css('font::text') if not p.css('strong::text').get() else p.css('strong::text')
            if name.get():
                item = Board()
                item['name'] = name.get()
                item['company'] = 'AstraZeneca'

                title = p
                print(title)
                item['title'] = title
                item['year'] = self.find_year(url)
                yield item

    def parse_prior_2002(self, response):
        url = response.request.url
        tables = response.css('table')
        cells = tables[17].css('td')
        for i, cell in enumerate(cells):
            if i != 0:
                if i % 2 == 1:
                    item = Board()
                    item['company'] = 'AstraZeneca'
                    name = cell.css('b::text').get()
                    try:
                        name = [item.strip(' ') for item in name.split('\n')]
                        name = ' '.join(name)
                        item['name'] = name
                    except Exception as e:
                        print(e)
                        item['name'] = 0
                else:
                    title = cell.css('font::text').get()
                    try:
                        title = [item.strip(' ') for item in title.split('\n')]
                        title = ' '.join(title)
                        item['title'] = title
                    except Exception as e:
                        print(e)
                        item['title'] = 0
                    item['year'] = self.find_year(url)

                    yield item
"""
Useful links:
https://www.youtube.com/watch?v=ALizgnSFTwQ

"""

"""
A bunch of important notes:
- astrazeneca completely changed their board_page URLs in 2016. So previous designs have preivious URLs.
You must find a way to automate this
- the sitemap.xml strategy does not work well, for it only shows you the most RECENT change to a certain webpage.
I could not find anything about extracting older versions, or detecting if there have been any older versions.
Therefore the code for XML is useless :(, although you did learn a bit of stuff
- it does not seem possible to extract older sitemaps from Wayback Machine. Why?
- update: you can access SOME older sitemaps, for example HSBC. But note that this is in 'plain' text
whereas the astrazeneca one seems fancier, could hat be the reason why?
(tried this with unilever, that does seem to be the case! This is a problem!)
"""