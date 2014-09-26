# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_games import items


class SteamSpider(scrapy.Spider):
    name = "steam"
    allowed_domains = ["store.steampowered.com"]

    start_urls = (
        'http://store.steampowered.com/app/240',
    )

    def __init__(self, *args, **kwargs):
        super(SteamSpider, self).__init__(*args, **kwargs)

        url_prefix = 'http://store.steampowered.com/app/'
        self.start_urls = []
        json_data = open('data/apps.json')
        data = json.load(json_data)
        for app_details in data['applist']['apps']:
            self.start_urls.append(url_prefix + str(app_details['appid']))
        print "Num URLs:", len(self.start_urls)

    def parse(self, response):
        pieces = str.split(response.url, '/')
        if pieces[-2] != 'app':
            print "Non-App Page: ", response.url
            return

        name_path = response.xpath('//div[@class="apphub_AppName"]/text()').extract()
        if len(name_path) == 0:
            return

        item = items.ScrapyGamesItem()
        item['appid'] = pieces[-1]
        item['name'] = name_path[0]

        description_lines = response.xpath(
            '//div[@class="game_area_description"]/text()'
        ).extract()
        description_lines = [x.strip() for x in description_lines]
        item['description'] = " ".join(description_lines)

        metacritic_path = response.xpath('//div[@id="game_area_metalink"]/a/@href').extract()
        if len(metacritic_path) == 0:
            return
        item['metacritic_url'] = metacritic_path[0]
        yield item