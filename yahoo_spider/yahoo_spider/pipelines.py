# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date

today = date.today().strftime('%Y-%m-%d')

def strQ2B(ustring):
    """把字符串全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        elif inside_code == 0x3002:
            inside_code = 0x2e
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:
            rstring += uchar
        else:
            rstring += chr(inside_code)
    return rstring


import logging
import pymongo
import six

MONGODB_ITEM_ID_FIELD = "_id"
logger = logging.getLogger(__name__)


class MongoDBPipeline(object):
    """
    爬蟲資料存Mongodb
    """

    def __init__(self, mongodb_server, mongodb_port, mongodb_db, mongodb_collection, mongodb_uniq_key,
                 mongodb_item_id_field, mongodb_item_cache):

        # self.connection = pymongo.MongoClient(mongodb_server, mongodb_port)
        self.connection = pymongo.MongoClient(mongodb_server)

        self.mongodb_db = mongodb_db
        self.db = self.connection[mongodb_db]
        self.mongodb_collection = mongodb_collection
        if mongodb_collection:
            self.collection = self.db[mongodb_collection]
        else:
            self.collection = None
        self.uniq_key = mongodb_uniq_key
        self.item_id = mongodb_item_id_field
        self.item_cache = mongodb_item_cache

        self.items = []

        if isinstance(self.uniq_key, six.string_types) and self.uniq_key == "":
            self.uniq_key = None

        if self.uniq_key:
            self.collection.create_index(self.uniq_key, unique=True)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('MONGODB_SERVER', 'localhost'), settings.get('MONGODB_PORT', 27017),
                   settings.get('MONGODB_DB', None), settings.get('MONGODB_COLLECTION', None),
                   settings.get('MONGODB_UNIQ_KEY', None), settings.get('MONGODB_ITEM_ID_FIELD', MONGODB_ITEM_ID_FIELD),
                   settings.get('MONGODB_ITEM_CACHE', 1000))

    def process_item(self, item, spider):
        for key, value in item.items():
            if type(value) is str:
                item[key] = strQ2B(value.strip())

        item['enqueue_date'] = today

        if self.mongodb_collection:
            self.items.append(item)

            if len(self.items) == self.item_cache:
                if self.uniq_key is None:
                    self.collection.insert_many(self.items, ordered=False)
                else:
                    for item in self.items:
                        self.collection.update_one({self.uniq_key: item[self.uniq_key]}, {'$set': item},
                                                   upsert=True)
                self.items = []
        else:
            table_name = item.pop('table')
            self.db[table_name].insert(item)

        return item

    def close_spider(self, spider):
        if self.mongodb_collection:
            if self.uniq_key is None and self.items:
                self.collection.insert_many(self.items, ordered=False)
            else:
                if self.uniq_key and self.items:
                    for item in self.items:
                        self.collection.update_one({self.uniq_key: item[self.uniq_key]}, {'$set': item},
                                                   upsert=True)
        self.connection.close()

