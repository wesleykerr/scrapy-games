scrapy-games
============

Infrastructure for scraping gaming websites.


## Crawl Steam

`wget http://api.steampowered.com/ISteamApps/GetAppList/v0002/ -O apps.json`
`scrapy crawl steam &> output.log &`

## Crawl Metacritic (to get review urls)

`scrapy crawl metacritic -o metacritic.json`
