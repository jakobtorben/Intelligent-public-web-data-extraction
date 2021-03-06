import scrapy
import random
import numpy as np
import re
import lxml.etree
import lxml.html
import nltk
from nltk.tokenize import word_tokenize

from ..items import ScrapyNavigatorItem

class HsbcSpider(scrapy.Spider):
    name = 'HSBC'
    allowed_domains = ['hsbc.com']
    start_urls = ['https://www.hsbc.com/who-we-are']
    
    def __init__(self):
        self.global_list = []
        self.ignore_status = ['403', '404']
        self.max_requests = 1000
        self.count = 0
        self.action_keywords = ["leadership", "board", "directors", "corporate", "about", "our", "executive", "team", "company"]
        self.relevance_keyword = ["title", "director", "board", "executive", "business", "chief", "group", "global", "officer",
                                  "commmittee", "member", "governance", "experience"]

    def start_requests(self):
        yield scrapy.Request('https://www.hsbc.com/who-we-are', callback = self.parse)
       

    # function that finds links on page and clicks them
    def parse(self, response):
        pageurl = []
        for href in response.css("a::attr('href')"):
            url = response.urljoin(href.extract())
            if url in self.global_list:
                continue
            if '#' in url:
                continue
            if "javascript:void(0)" in url:
                continue
            if "mailto" in url:
                continue
            if scrapy.http.Response(url).status in self.ignore_status:
                continue
            pageurl.append(url)
            yield scrapy.Request(url, callback = self.parse_attr)

        new_urls = self.page_agent(pageurl, 2)
        for new_url in new_urls:
            if (self.count < self.max_requests):
                yield scrapy.Request(new_url, callback = self.parse)


    def parse_attr(self, response):
        item = ScrapyNavigatorItem()
        item['link'] = response.url
        item['relevance'] = self.relevance(response)
        item['action_vec'] = self.action_vector(response.url)
        state_vec = np.array([item['relevance'], item['action_vec'][0] ])
        item['state_vec'] = state_vec
        self.count += 1
        return item

    
    def page_agent(self, pageurl, size):
        new_urls = []
        for url in range(size):
            valid = False
            while (valid == False):
                selection = random.randint(0, len(pageurl)-1)
                if pageurl[selection] not in new_urls:
                    valid = True
                elif scrapy.response(pageurl[selection]).status in self.ignore_status:
                    valid = False
                    
            new_urls.append(pageurl[selection])
        return new_urls


    def relevance(self, response):
        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

        # complete text
        text = lxml.html.tostring(root, method="text", encoding='unicode')
        text = text.lower()
        text_tokens = word_tokenize(text)
        length = len(text_tokens)
        if length == 0:
            return 0
        rel = 0
        for kword in self.relevance_keyword:
            rel += text_tokens.count(kword)
        rel /= length
        return rel


    def action_vector(self, suburl):
        vec = np.zeros(2)

        linkwords = re.findall(r"[\w']+", suburl)
        for word in linkwords:
            if word in self.action_keywords:
                vec[0] += 1
        vec[0] /= len(linkwords)

        # Ideally add method to search text around link and add metric to vec[1]
        return vec