from django.db import models
from datetime import datetime


class Feature(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=500)


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100000)
    file_data = models.CharField(max_length=100, null=True)
    create_at = models.DateTimeField(default=datetime.now(), blank=True)


class SaveFileField(models.Model):
    save_file = models.FileField()
