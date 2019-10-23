import ctypes
import urllib
import requests
from retrying import retry
import time
import sys
import logging as log

log.basicConfig(filename='sample.log', level=log.INFO)
WALLPAPER_URL = 'http://www.reddit.com/r/wallpapers/.json'
SPI_SETDESKWALLPAPER = 20
headers = {
    'User-Agent': 'me'
}


def log_exception(exctype, value, tb):
    log.error("Uncaught exception", exc_info=(exctype, value, tb))


sys.excepthook = log_exception


@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=3600000)
def is_connected():
    log.info('ensuring network connection...')
    urllib.urlopen('http://www.reddit.com')


is_connected()


def unicode_to_utf8(input):
    if isinstance(input, dict):
        return {unicode_to_utf8(key): unicode_to_utf8(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [unicode_to_utf8(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def get_data(after=False, count=0):
    if after:
        page_url = WALLPAPER_URL + '?count=' + str(count) + '&after=' + after
        log.info("NEW PAGE: "+ page_url)
    else:
        page_url = WALLPAPER_URL
    r = requests.get(page_url, headers=headers)
    if r.status_code is 200:
        log.info("successfully got new page")
        return unicode_to_utf8(r.json())
    else:
        log.info(r.status_code)
        return False


image = urllib.URLopener()
image.addheader('User-Agent', 'me')
not_finished = True
data = get_data()
total_images = 0

while not_finished:
    not_finished = False
    total_images += 25
    for i, post in enumerate(data['data']['children'], 1):
        if post['data']['over_18'] is True or post['data']['stickied'] is True:
            continue
        try:
            url = post['data']['preview']['images'][0]['source']['url']
        except KeyError, e:
            log.error('no preview available: ' + str(e))
            continue
        url = url.replace("amp;s", "s")
        log.info("getting: " + url + "image num: {0}".format(str(i)))

        image.retrieve(
            url,
            "C:\\Users\\Robbie\\Pictures\\Wallpapers\\desktop.jpg")
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0,
                                                   "C:\\Users\\Robbie\\Pictures\\Wallpapers\\desktop.jpg", 3)
        if i is 25:
            data = get_data(after=data['data']['after'], count=total_images)
            if data:
                log.info("Not finished, loop again")
                not_finished = True
            else:
                log.info("No more data, finished")
                not_finished = False
        time.sleep(10 * 60)
