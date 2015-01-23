#!/bin/bash

# this file will contain environment variables that 
# will not be checked into source control
source overrides

apt-get update
apt-get upgrade

apt-get install git 

apt-get install -y python2.7 python2.7-dev python-setuptools python-pip python-lxml python-bs4 ipython

pip install scrapy

debconf-set-selections <<< 'mysql-server mysql-server/root_password password $ROOT_PASSWORD'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password $ROOT_PASSWORD'

apt-get install mysql-server mysql-client libmysqlclient-dev

pip install peewee
pip install mysql-python


