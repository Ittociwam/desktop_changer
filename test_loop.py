import urllib
import logging as log
import sys
from retrying import retry

log.basicConfig(filename='sample.log', level=log.INFO)


def log_exception(exctype, value, tb):
	log.error("Uncaught exception", exc_info=(exctype, value, tb))

sys.excepthook = log_exception

log.info('hello')

a = {'key': 'value'}


b = a['ke']

print b
