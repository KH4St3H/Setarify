from django.contrib.auth.models import User
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    cover = models.ImageField(upload_to='artists-covers/', null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='artist')

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    cover = models.ImageField(upload_to='albums-covers/', null=True, blank=True)
    release_date = models.DateField(blank=True, null=True)
    artist = models.ManyToManyField(Artist, related_name='artists')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    genre = models.CharField(max_length=100)
    file_url = models.URLField(blank=True, null=True)
    cover = models.ImageField(upload_to='song-covers/', null=True, blank=True)
    release_date = models.DateField(blank=True, null=True)

    artist = models.ManyToManyField(Artist, related_name='songs')
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL, related_name='songs')

    hit_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='playlist-covers/', null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PlaylistSong(models.Model):
    order = models.PositiveIntegerField()
    song = models.ForeignKey(Song, null=True, on_delete=models.SET_NULL)
    playlist = models.ForeignKey(Playlist, null=True, on_delete=models.CASCADE, related_name='songs')

    class Meta:
        unique_together = ('song', 'playlist')
        ordering = ['order']


class Like(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, null=True, on_delete=models.CASCADE, related_name='likes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'song')
