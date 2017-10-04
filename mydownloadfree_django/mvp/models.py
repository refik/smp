from django.db import models


class App(models.Model):
    name = models.CharField(max_length = 500)
    logo_url = models.CharField(max_length = 500)
    article = models.TextField()
