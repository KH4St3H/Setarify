from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Artist, Album, Song, Playlist, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['slug', 'name']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['title', 'slug']


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    album = AlbumSerializer(read_only=True)
    class Meta:
        model = Song
        fields = ['title', 'slug', 'genre', 'artist', 'album']


class PlaylistSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = ['title', 'slug', 'author', 'song']