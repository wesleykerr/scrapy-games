__author__ = 'wkerr'
import datetime
import logging
from peewee import *

# First run:
#  CREATE DATABASE steam_db;
#  CREATE USER 'steam_user'@'localhost';
#  GRANT ALL ON steam_db.* TO 'steam_user'@'localhost';
db = MySQLDatabase('steam_db', user='steam_user')

class BaseModel(Model):
    class Meta:
        database = db

class Steam(BaseModel):
    steam_id = BigIntegerField(primary_key=True)
    steam_url = CharField(max_length=512, null=True)
    title = CharField(max_length=256, null=True)
    description = TextField(null=True)
    metacritic_score = IntegerField(null=True)
    metacritic_url = CharField(max_length=512, null=True)
    last_indexed = DateTimeField(null=True)
    html = TextField(null=True)

class SteamTag(BaseModel):
    steam_id = BigIntegerField(null=False)
    name = CharField(max_length=128)

    class Meta:
        primary_key = CompositeKey('steam_id', 'name')


class SteamImage(BaseModel):
    steam_id = BigIntegerField(null=False)
    img_url = CharField(max_length=256)
    last_indexed = DateTimeField(null=True)

    class Meta:
        primary_key = CompositeKey('steam_id', 'img_url')


class ReviewDetails(BaseModel):
    steam_id = BigIntegerField()
    metacritic_url = CharField(max_length=512)
    review_url = CharField(max_length=512)
    reviewer = CharField(max_length=256)
    description = TextField()
    score = IntegerField()


class Review(BaseModel):
    steam_id = BigIntegerField()
    metacritic_url = CharField(max_length=512)
    orig_review_url = CharField(max_length=512)
    review_url = CharField(max_length=512)
    html = TextField()


def add_steam_details_to_db(steam_id, url, html, soup):
    try:
        with db.transaction():
            create_steam_details(steam_id, url, html, soup)
            create_steam_tags(steam_id, soup)
            create_steam_images(steam_id, soup)

    except IntegrityError:
        logging.error('IntegrityError %s' % str(steam_id))

def create_steam_details(steam_id, url, html, soup):
    steam = Steam.create(steam_id=steam_id)
    steam.steam_url = url
    steam.html = html
    title_div = soup.find('div', {'class': 'apphub_AppName'})
    if title_div:
        steam.title = title_div.text

    description_div = soup.find('div', {'id': 'game_area_description'})
    if description_div:
        steam.description = description_div.text

    release_date_div = soup.find('span', {'class': 'date'})
    if release_date_div:
        # set the release date div.
        date = release_date_div.text

    metacritic_div = soup.find('div', {'id': 'game_area_metalink' })
    if metacritic_div:
        if metacritic_div.find('a'):
            steam.metacritic_url = metacritic_div.find('a').get('href')

    metacritic_score_div = soup.find('div', {'id': 'game_area_metascore'})
    if metacritic_score_div:
        if metacritic_score_div.find('span'):
            steam.metacritic_score = int(metacritic_score_div.find('span').text)

    steam.last_indexed = datetime.datetime.now()
    steam.save()
    return True, steam


def create_steam_tags(steam_id, soup):
    num_tags = 0
    tags_div = soup.find('div', {'class': 'glance_tags popular_tags'})
    if tags_div:
        for tag in tags_div.find_all('a'):
            SteamTag.create(steam_id=steam_id, name=tag.text.strip())
            num_tags += 1
    else:
        logging.warn("Missing Tags %s" % str(steam_id))
    return True, num_tags


def create_steam_images(steam_id, soup):
    num_screenshots = 0
    screen_shots_div = soup.find_all('div', {'class': 'highlight_strip_screenshot'})
    if screen_shots_div:
        for screen_shot_div in screen_shots_div:
            img_src = screen_shot_div.find('img').get('src')
            try:
                SteamImage.create(steam_id=steam_id, img_url=img_src, last_indexed=None)
                num_screenshots += 1
            except IntegrityError:
                print "duplicate: ", steam_id, img_src
    else:
        logging.warn("Missing screen shots %s" % str(steam_id))
    return True, num_screenshots