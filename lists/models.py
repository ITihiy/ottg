from django.db import models
from django.shortcuts import reverse


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey('List', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')


class List(models.Model):
    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])
