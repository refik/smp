# -*- coding: utf-8 -*-

from mvp.models import ScrapedItem
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapySmpPipeline(object):
    def process_item(self, item, spider):
        meta = item.pop('scrapy_meta')
        scraped_item = ScrapedItem(**meta, item = json.dumps(item))
        scraped_item.save()