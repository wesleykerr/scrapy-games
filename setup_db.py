#!/usr/bin/python
__author__ = 'wkerr'

from peewee import *
from scrapy_games.models import models

# First run:
#  CREATE DATABASE steam_db;
#  CREATE USER 'steam_user'@'localhost';
#  GRANT ALL ON steam_db.* TO 'steam_user'@'localhost';
db = MySQLDatabase('steam_db', user='steam_user')
db.connect()
db.create_tables([models.Steam, models.SteamTag, models.SteamImage])
