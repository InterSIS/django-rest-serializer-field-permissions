from django.db import models


class Album(models.Model):
    album_name = models.TextField()
    artist = models.TextField()
    diary = models.TextField()


class Track(models.Model):
    duration = models.IntegerField()
    order = models.TextField()
    title = models.TextField()
    album = models.ForeignKey(to=Album, related_name='tracks', on_delete=models.CASCADE)
