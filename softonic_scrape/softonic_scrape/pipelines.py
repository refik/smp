# -*- coding: utf-8 -*-

from mvp.models import App

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SoftonicScrapePipeline(object):
    def process_item(self, item, spider):
        item.pop('categories')
        app = App(**item)
        app.save()