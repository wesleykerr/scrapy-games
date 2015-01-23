# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_games project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapy_games'

SPIDER_MODULES = ['scrapy_games.spiders']
ITEM_PIPELINES = {
    'scrapy_games.pipelines.DatabasePipeline': 100,
    'scrapy_games.pipelines.ReviewsPipeline': 101,
}

NEWSPIDER_MODULE = 'scrapy_games.spiders'
DOWNLOAD_DELAY = 2

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'steamrecommender (+http://www.steamrecommender.com)'
