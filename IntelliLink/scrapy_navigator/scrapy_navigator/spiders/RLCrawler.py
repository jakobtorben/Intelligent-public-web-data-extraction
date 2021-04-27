import scrapy
import random
import numpy as np
import re
import lxml.etree
import lxml.html
import nltk
from nltk.tokenize import word_tokenize
from spiderNet import *
import torch

from ..items import ScrapyNavigatorItem

class RlcrawlerSpider(scrapy.Spider):
    name = 'RLCrawler'
    allowed_domains = ['hsbc.com']
    start_urls = ['https://www.hsbc.com/who-we-are']
    
    def __init__(self):
        # scrapy spider variables
        self.global_list = []
        self.ignore_status = ['403', '404']
        self.max_requests = 1000
        self.count = 0
        self.action_keywords = ["leadership", "board", "directors", "corporate", "about", "our", "executive", "team", "company"]
        self.relevance_keyword = ["title", "director", "board", "executive", "business", "chief", "group", "global", "officer",
                                  "commmittee", "member", "governance", "experience"]
        
        
        # spidernet variables
        # set input dimension to 3 because state + action vector is size 3
        self.spiderNet = spiderNet(input_dimension=3)
        self.epsilon = 1
        self.epsilon_decay = 0.9
        self.stateVector = None
        self.actionVector = None
        self.buffer = spiderNet.ReplayBuffer()

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
            #yield scrapy.Request(url, callback = self.parse_attr)

        new_url = self.page_agent(response, pageurl)
        #for new_url in new_urls:
        if (self.count < self.max_requests):
            self.coutn += 1
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

    
    def page_agent(self, response, pageurl):

        valid = False
        while (valid == False):
            
            reward = self.relevance(response)
            self.actionVector = self.action_vector(response.url)
            self.stateVector = np.array(reward, self.actionVector[0])
            state_action_vector = self.state_vector + self.action_vector  
            # is this what we want? this will make state action vector equal to
            # ind 0 = relevance + relevance of url
            # ind 1 = relevance of url + 0
            # did you mean to create a new vector of length 4?
            
            # Create a transition
            transition = (self.state_vector, self.action_vector, reward, next_state)
            # append transition to buffer
            self.buffer.append_to_buffer(transition)
            
            Q = self.spiderNet.network.forward(torch.tensor(state_action_vector).unsqueeze(0))
            
            greedy_action = np.argmax(Q[0].detach().numpy())
            
            # modify selection here
            # epsilon greedy behaviour
            if random.uniform(0,1) < self.epsilon:
                selection = random.randint(0, len(pageurl)-1)
            else:
                selection = greedy_action
                
            #if pageurl[selection] not in new_urls:
            #    valid = True
            if scrapy.response(pageurl[selection]).status in self.ignore_status:
                valid = False

        new_url = pageurl[selection] 
        #new_urls.append(pageurl[selection])
        return new_url


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