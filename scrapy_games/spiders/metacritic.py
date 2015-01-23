# -*- coding: utf-8 -*-
import scrapy
from scrapy_games import items
from scrapy_games.models import models

MAX_URLS = -1
BASE_URL = 'http://www.metacritic.com'

class MetacriticSpider(scrapy.Spider):
    name = "metacritic"

    pipelines = [
        'ReviewsPipeline'
    ]

    def __init__(self, *args, **kwargs):
        super(MetacriticSpider, self).__init__(*args, **kwargs)


    def start_requests(self):
        requests = []
        for game in models.Steam.select().where(models.Steam.metacritic_url != 'NULL'):
            request = scrapy.Request(game.metacritic_url, callback=self.parse)
            request.meta['steam_id'] = game.steam_id
            requests.append(request)

            if MAX_URLS != -1 and len(requests) >= MAX_URLS:
                break
        return requests


    def parse(self, response):
        critic_reviews = response.xpath('//div[@class="module reviews_module critic_reviews_module"]')
        all_reviews_url = critic_reviews.xpath('.//p[@class="see_all"]/a/@href').extract()
        if all_reviews_url:
            request = scrapy.Request(BASE_URL + all_reviews_url[0],
                                     callback=self.parse_metacritic_reviews)
            request.meta['metacritic_url'] = response.url
            request.meta['steam_id'] = response.request.meta['steam_id']
            yield request
        else:
            request = scrapy.Request(response.url, callback=self.parse_metacritic_reviews)
            request.meta['metacritic_url'] = response.url
            request.meta['steam_id'] = response.request.meta['steam_id']
            yield request


    def parse_metacritic_reviews(self, response):
        subselect = response.xpath('//div[@class="module reviews_module critic_reviews_module"]')
        reviews = subselect.xpath('.//div[@class="review_content"]')
        for selector in reviews:
            review_item = items.ReviewItem()
            review_item['steam_id'] = response.request.meta['steam_id']
            review_item['metacritic_url'] = response.request.meta['metacritic_url']

            source_text = selector.xpath('.//div[@class="source"]/a/text()').extract()
            if source_text:
                review_item['reviewer'] = source_text[0].strip()

            body_text = selector.xpath('.//div[@class="review_body"]/text()').extract()
            if body_text:
                review_item['description'] = body_text[0].strip()

            score_text = selector.xpath('.//div[@class="review_grade"]/div/text()').extract()
            if score_text:
                review_item['score'] = score_text[0].strip()

            url = selector.xpath('.//li[@class="review_action full_review"]/a/@href').extract()

            if url:
                review_item['review_url'] = url[0]
                yield review_item

                request = scrapy.Request(url[0], callback=self.parse_review)
                request.meta['steam_id'] = response.request.meta['steam_id']
                request.meta['metacritic_url'] = response.request.meta['metacritic_url']
                yield request

    def parse_review(self, response):
        if response.status == 404:
            self.log("Received 404: %s" % response.request.url)
            return

        item = items.ReviewHtmlItem()
        item['steam_id'] = response.request.meta['steam_id']
        item['metacritic_url'] = response.request.meta['metacritic_url']
        item['orig_review_url'] = response.request.url
        item['review_url'] = response.url
        item['html'] = response.body.decode(response.encoding)
        yield item

