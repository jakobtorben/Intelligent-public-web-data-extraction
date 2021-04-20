# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyNavigatorItem(scrapy.Item):
    link = scrapy.Field()
    relevance = scrapy.Field()
    action_vec = scrapy.Field()
    state_vec = scrapy.Field()
