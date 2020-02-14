# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class HomeworkScrapyItem(scrapy.Item):
    title = scrapy.Field()
    word1 = scrapy.Field()
    word2 = scrapy.Field()
    word3 = scrapy.Field()
    author = scrapy.Field()
    author_img = scrapy.Field()
    time = scrapy.Field()
    viewnum = scrapy.Field()
    content = scrapy.Field()
    introduction = scrapy.Field()

