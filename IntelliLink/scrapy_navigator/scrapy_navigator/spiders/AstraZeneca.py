import scrapy
import random
import re
from ..items import ScrapyNavigatorItem
import pandas as pd


path_to_people = '/Users/yousefnami/Desktop/Yousef/Imperial/Extra Curricular/ICDSS/Intelligent-public-web-data-extraction/ManWebScraper/AstraZeneca_board.csv'

class AstraZenecaSpider(scrapy.Spider):
    name = 'AstraZeneca'
    # allowed_domains = ['wwAstraZeneca.com']
    start_urls = ['https://www.astrazeneca.com']

    # function that finds links on page and clicks them
    def parse(self, response):
        """ Collect links from the mainpage, currently does not support recursion """

        for href in response.xpath("//a[not(contains(@href, '#'))]/@href"):
            # TODO remove dupliate urls
            url = response.urljoin(href.extract())

            print(url)

            #if url == 'https://www.astrazeneca.com/our-company.html':
            yield scrapy.Request(url, callback = self.parse_tags)
            #    break

    def parse_test(self, response):

        item = response.body
        print(clean_html(str(item)))


    # function that deals with pages returned from above
    def parse_dir_contents(self, response):
        item = ScrapyNavigatorItem()
        for sel in response.xpath('//ul/li'):
            # TODO @ricardo not sure what this is doing? is it doing parse again but at the
            # TODO link level as opposed to mainpage? Not convincedim
            print(sel)
            item['link'] = sel.xpath('a/@href').extract()
            print(item['link'])
            yield item

    def create_dataset(self, **kwargs):
        item = ScrapyNavigatorItem()

        # asign fields
        for kw, arg in kwargs.items():
            item[kw] = arg
        return item

    def parse_tags(self, response):
        html_text = str(response.body)
        # TODO clean this up, not very elegant..
        # PATH to CSV containing names of CEOs and Board members

        df = pd.read_csv('ENTER PATH')
        names = list(df.name.values)
        count = 0
        save_names = []
        for name in names:
            name_components = name.split()
            for component in name_components:
                matches = re.findall(f"(?<![\w])(?i){component}(?![\w])", html_text)
                if matches:
                    count += len(matches)
                    # TODO need to add smth to normalize the counts
                    if name not in save_names:
                        save_names.append(name)
        if count:
            title = response.css('title::text').get()
            # TODO not sure if this will generalise? but seems standard?
            meta = response.css('meta[name=description]::attr(content)').get()
            yield self.create_dataset(link = response.request.url, count = count, names = save_names, title = title, meta= meta)
        # TODO add code to get code from eikon?
        # (for now just using simple pandas)

    def parse_newspaper(self, ):
        """ Some testing was done on newspaper library. Not successful."""
        pass

def clean_html(text):
    """ NOT RELEVANT ATM """
    # removes html tags
    cleaner = re.compile('<.*?>')
    text = re.sub(cleaner, '', text)

    # removes \n characters that are actually str of \ + n
    text = re.sub(r'\\n', ' ', text)
    # removes html classes # TODO expand this to include other html attribs
    text = re.sub('class=', ' ', text)

    # removes any texts in brackets
    text = re.sub(r'\{.*?\}', ' ', text)
    text = re.sub(r'\[.*?\]', ' ', text)

    # removes commas
    text = re.sub(r',', ' ', text)

    # shrinks any whitespace to single whitespace
    text = re.sub(r"\s+", " ", text)

    # text = re.sub(keep_letters, '', text)

    # print(text)
    # text = re.sub(r'[\\\/\+\(\-\*\)]', ' ', text)
    # text =  re.sub(r"(?<!\_)[0-9]", '', text)
    return text


