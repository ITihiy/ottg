from django.db import models


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey('List', on_delete=models.CASCADE)


class List(models.Model):
    pass
