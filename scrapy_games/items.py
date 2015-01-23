# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class ScrapyGamesItem(scrapy.Item):
    steam_id = scrapy.Field()
    steam_url = scrapy.Field()
    html = scrapy.Field()

class MetacriticItem(scrapy.Item):
    metacritic_url = scrapy.Field()
    num_reviews = scrapy.Field()
    all_reviews_url = scrapy.Field()
    review_urls = scrapy.Field()

class ReviewItem(scrapy.Item):
    steam_id = scrapy.Field()
    metacritic_url = scrapy.Field()
    review_url = scrapy.Field()
    reviewer = scrapy.Field()
    description = scrapy.Field()
    score = scrapy.Field()

class ReviewHtmlItem(scrapy.Item):
    steam_id = scrapy.Field()
    metacritic_url = scrapy.Field()
    orig_review_url = scrapy.Field()
    review_url = scrapy.Field()
    html = scrapy.Field()

