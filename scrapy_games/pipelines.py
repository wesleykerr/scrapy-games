# -*- coding: utf-8 -*-
#
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from bs4 import BeautifulSoup
from peewee import *
from scrapy.exceptions import DropItem
from scrapy_games import items
from scrapy_games.models import models


class DatabasePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if 'DatabasePipeline' not in getattr(spider, 'pipelines'):
            return item

        soup = BeautifulSoup(item['html'])
        page_header = soup.find('h2', {'class': 'pageheader'})
        if page_header and page_header.text.strip() == 'Oops, sorry!':
            logging.warning("Dropping %s" % str(item['steam_id']))
            raise DropItem("Unavailable %s" % str(item['steam_id']))

        models.add_steam_details_to_db(
            item['steam_id'], item['steam_url'], item['html'], soup)

        return item


class ReviewsPipeline(object):
    def process_item(self, item, spider):
        if 'ReviewsPipeline' not in getattr(spider, 'pipelines'):
            return item

        if isinstance(item, items.ReviewItem):
            self.add_review_item(item)
        elif isinstance(item, items.ReviewHtmlItem):
            self.add_review_html_item(item)

        return item

    def add_review_item(self, item):
        review = models.ReviewDetails.create(steam_id=item['steam_id'])
        review.metacritic_url = item['metacritic_url']
        review.review_url = item['review_url']
        review.reviewer = item['reviewer']
        review.description = item['description']
        review.score = item['score']
        review.save()

    def add_review_html_item(self, item):
        review = models.Review.create(steam_id=item['steam_id'])
        review.metacritic_url = item['metacritic_url']
        review.orig_review_url = item['orig_review_url']
        review.review_url = item['review_url']
        review.html = item['html']
        review.save()