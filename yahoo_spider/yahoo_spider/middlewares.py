# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from pyquery import PyQuery
import unicodedata


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")


class PyQueryMiddleware(object):
    def __init__(self, parser):
        self.parser = parser

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('PyQueryPARSER', None))

    def process_response(self, request, response, spider):
        try:
            if response.text:
                response.dom = PyQuery(remove_control_characters(response.text), parser=self.parser)
        except AttributeError:
            pass
        return response
