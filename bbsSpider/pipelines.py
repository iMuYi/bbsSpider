# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import BbsspiderItem
from scrapy.conf import settings
import pymongo

class BbsspiderPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        print 'open_spider'
        self.f = open('spider.log','w')
        HOST = settings['MONGODB_HOST']
        PORT = settings['MONGODB_PORT']
        DB = settings['MONGODB_DBNAME']
        COLLECTION = settings['MONGODB_DOCNAME']
        CLIENT = pymongo.MongoClient(host=HOST, port=PORT)
        db = CLIENT[DB]
        self.collection = db[COLLECTION]

    def process_item(self, item, spider):
        PartTime = dict(item)
        POSTS = {"title": PartTime['title'],
                 "url": "http://bbs.byr.cn"+PartTime['url'],
                 "time": PartTime['time'],
                 }
        if "python" in PartTime['html'] or "Python" in PartTime['html'] or "PYTHON" in PartTime['html']:
            try:
                result = self.collection.find({"url":POSTS['url']})
                result.next()
            except StopIteration:
                self.collection.insert(POSTS)
        return item

    def close_spider(self, spider):
        print 'close_spider'
        self.f.close()
