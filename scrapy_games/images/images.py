
from datetime import datetime
import logging
import time
import urlparse
import wget
from scrapy_games.models import models


OUTPUT_DIR = '/vagrant/data/images'

def download_image(img_url, output_file):
    wget.download(img_url, out=output_file)
    return True

def main():
    for image in models.SteamImage.select().where(models.SteamImage.last_indexed >> None):
        # Download the image at full size.
        if not '116x65' in image.img_url:
            logging.warn('missing size details: %s', image.img_url)
            continue

        image_url = image.img_url.replace('116x65.', '')
        url_parse = urlparse.urlparse(image_url)
        parts = url_parse.path.split('/')

        if download_image(image_url, '%s/%s_%s' % (OUTPUT_DIR, parts[-2], parts[-1])):
            image.last_indexed = datetime.today()
            image.save()
        else:
            logging.warn('unable to download: [%s] %s', image.steam_id, image_url)
        time.sleep(1.5)

if __name__ == "__main__":
    main()