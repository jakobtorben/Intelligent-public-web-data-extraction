import scrapy
import lxml.etree
import lxml.html
from collections import Counter
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

#from items import ScrapyNavigatorItem

class DatabaseSpider(scrapy.Spider):
    name = 'database'

    def __init__(self):
        self.global_text = ""
        self.count = 0

    def start_requests(self):
        yield scrapy.Request('https://www.hsbc.com/who-we-are/leadership-and-governance/board-of-directors', callback = self.parse, meta = {"company": "HSBC"})
        yield scrapy.Request('https://www.bhp.com/our-approach/our-company/leadership-team/', callback = self.parse, meta = {"company": "BHP Group"}) 
        yield scrapy.Request('http://www.unilever.com/about/who-we-are/our-leadership/', callback = self.parse, meta = {"company": "Unilever"})
        yield scrapy.Request('https://www.shell.com/about-us/leadership/executive-committee.html', callback = self.parse, meta = {"company": "Royal Dutch Shell"})
        yield scrapy.Request('https://www.riotinto.com/about/board-of-directors', callback = self.parse, meta = {"company": "Rio Tinto"})
        yield scrapy.Request('https://www.astrazeneca.com/our-company/leadership.html', callback = self.parse, meta = {"company": "Astrazeneca"})
        yield scrapy.Request('https://www.diageo.com/en/our-business/board-of-directors/', callback = self.parse, meta = {"company": "Diageo"})
        yield scrapy.Request('https://www.gsk.com/en-gb/about-us/corporate-executive-team', callback = self.parse, meta = {"company": "GlaxoSmithKline"})
        yield scrapy.Request('https://www.bat.com/group/sites/UK__9D9KCY.nsf/vwPagesWebLive/DOBB9HYM', callback = self.parse, meta = {"company": "British American Tobacc"})
        yield scrapy.Request('https://www.bp.com/en/global/corporate/who-we-are/board-and-executive-management/the-board.html', callback = self.parse, meta = {"company": "BP"})
        

    def parse(self, response):
        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

        # complete text
        text = lxml.html.tostring(root, method="text", encoding='unicode')
        text = text.lower()
        self.global_text += text
        self.count += 1

        # find most common word on one site
        text_tokens = word_tokenize(text)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words() if word.isalpha()]
        dict_word = Counter(tokens_without_sw)

        with open( response.meta.get('company') + '.csv', 'w', encoding="utf-8") as csv_file:  
            for key, value in dict_word.most_common():
                    csv_file.write( "{}, {}\n".format(key,value))

        # find global sum
        if (self.count == 10):
            global_text_tokens = word_tokenize(self.global_text)
            global_tokens_without_sw = [word for word in global_text_tokens if not word in stopwords.words() if word.isalpha()]
            global_dict_word = Counter(global_tokens_without_sw)

            with open('global_sum.csv', 'w', encoding="utf-8") as csv_file:  
                for key, value in global_dict_word.most_common():
                     csv_file.write( "{}, {}\n".format(key,value))

