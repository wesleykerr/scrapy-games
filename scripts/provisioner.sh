#!/bin/bash

# this file will contain environment variables that 
# will not be checked into source control
source overrides

apt-get update
apt-get upgrade

apt-get install git 

apt-get install -y python2.7 python2.7-dev python-setuptools python-pip python-lxml

pip install scrapy

debconf-set-selections <<< 'mysql-server mysql-server/root_password password $ROOT_PASSWORD'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password $ROOT_PASSWORD'

apt-get install mysql-server mysql-client

pip install peewee

wget http://sourceforge.net/projects/liquibase/files/Liquibase%20Core/liquibase-3.2.2-bin.tar.gz/download -O liquibase-bin.tar.gz

mkdir -p /usr/local/share/liquibase
tar -zxvf liquibase-bin.tar.gz -C /usr/local/share/liquibase

