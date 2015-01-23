# -*- coding: utf-8 -*-
import json
import logging
import scrapy
from scrapy_games import items

APP_PREFIX = 'http://store.steampowered.com/app/'
APP_LIST = 'http://api.steampowered.com/ISteamApps/GetAppList/v2'
COOKIES = {'birthtime':'294390001'}

USE_DEBUG_URLS = False


class SteamSpider(scrapy.Spider):
    name = "steam"
    allowed_domains = ["store.steampowered.com"]

    start_urls = [
        'http://store.steampowered.com/app/906',  # Rag Doll Kung Fu Trailer
        'http://store.steampowered.com/app/4230',  # Race: The WTCC Game
        'http://store.steampowered.com/app/72850',  # The Elder Scrolls V: Skyrim
        'http://store.steampowered.com/app/570',  # Dota 2
        'http://store.steampowered.com/app/575',  # Dota 2 - English Depot
        'http://store.steampowered.com/app/10410',  # Futbol Manager 2008 (not available)
    ]
    pipelines = [
       'DatabasePipeline'
    ]

    def __init__(self, *args, **kwargs):
        super(SteamSpider, self).__init__(*args, **kwargs)

        if not USE_DEBUG_URLS:
            self.start_urls = []
            json_data = open('data/apps.json')
            data = json.load(json_data)
            for app_details in data['applist']['apps']:
                self.start_urls.append(APP_PREFIX + str(app_details['appid']))
            print "Num URLs:", len(self.start_urls)


    def start_requests(self):
        requests = []
        for url in self.start_urls:
            requests.append(scrapy.Request(url, callback=self.parse, cookies=COOKIES))
        return requests


    def parse(self, response):
        pieces = str.split(response.url, '/')
        if response.request.url != response.url and request.url.startswith(APP_PREFIX):
            logging.warn('Redirect-App %s %s' % (response.request.url, response.url))
            pass
        elif response.request.url != response.url:
            logging.warn('Redirect-NonApp %s %s' % (response.request.url, response.url))
            return

        if pieces[-2] != 'app':
            logging.warn('NonApp-Page %s %s' % (response.request.url, response.url))
            return

        item = items.ScrapyGamesItem()
        item['steam_id'] = pieces[-1]
        item['steam_url'] = response.url
        item['html'] = response.body.decode(response.encoding)
        yield item