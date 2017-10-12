from django.contrib.postgres.fields import JSONField
from django.db import models


class App(models.Model):
    name = models.CharField(max_length = 500)
    logo_url = models.CharField(max_length = 500)
    article = models.TextField()

class ScrapedItem(models.Model):
    request_url = models.CharField(max_length = 500)
    parent_url = models.CharField(max_length=500, null=True)
    request_time = models.DateTimeField()
    spider_name = models.CharField(max_length = 500)
    callback_function = models.CharField(max_length=500)
    spider_load_time = models.DateTimeField()
    item = JSONField()