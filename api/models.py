from django.contrib.auth.models import User
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(blank=True, null=True)
    artist = models.ManyToManyField(Artist, related_name='artists')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Song(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    file_url = models.URLField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    artist = models.ManyToManyField(Artist, related_name='songs')
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL, related_name='songs')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'song')
