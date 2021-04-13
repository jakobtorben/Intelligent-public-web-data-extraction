# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyNavigatorItem(scrapy.Item):
    link = scrapy.Field()
    count = scrapy.Field()
    names = scrapy.Field()
    meta = scrapy.Field()
    title = scrapy.Field()
