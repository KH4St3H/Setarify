from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import HiddenField, BooleanField
from rest_framework.relations import SlugRelatedField

from api.models import Artist, Album, Song, Playlist, Like, PlaylistSong, SongFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['slug', 'name', 'cover']


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = ['title', 'slug', 'artist', 'cover']


class AlbumBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['title', 'slug', 'cover']


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True, many=True)
    album = AlbumBriefSerializer(read_only=True)
    album_slug = SlugRelatedField(slug_field='slug', queryset=Album.objects.all(), write_only=True)
    liked = BooleanField(read_only=True, default=False)

    class Meta:
        model = Song
        fields = ['title', 'slug', 'genre', 'artist', 'release_date', 'album', 'album_slug',
                  'cover', 'like_count', 'hit_count', 'liked']
        write_only_fields = ['file_url']

    def create(self, validated_data):
        if 'album_slug' in validated_data:
            album = validated_data.pop('album_slug')
        else:
            album = None

        song = super().create(validated_data)
        song.album = album
        return song


class SongBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['title', 'slug', 'cover']


class SongBriefWithArtistSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True, many=True)

    class Meta:
        model = Song
        fields = ['title', 'slug', 'artist', 'cover', 'like_count', 'hit_count']


class AlbumWithSongsSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True, many=True)
    songs = SongBriefSerializer(many=True)

    class Meta:
        model = Album
        fields = ['title', 'slug', 'artist', 'songs', 'cover']


class PlaylistSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = ['title', 'slug', 'author', 'cover']


class PlaylistSongSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    song_slug = SlugRelatedField(slug_field='slug', queryset=Song.objects.all(), write_only=True)

    class Meta:
        model = PlaylistSong
        fields = ['order', 'song', 'song_slug']

    def create(self, validated_data):
        if 'song_slug' not in validated_data:
            return super().create(validated_data)

        song = validated_data.pop('song_slug')
        playlist_song = super().create(validated_data)
        playlist_song.song = song
        playlist_song.save()
        return playlist_song


class PlaylistWithSongsSerializer(serializers.ModelSerializer):
    songs = PlaylistSongSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = ['title', 'slug', 'author', 'songs', 'cover']


class SongFileUrlSerializer(serializers.Serializer):
    file_url = serializers.URLField(read_only=True)

    class Meta:
        fields = ['file']


class SongFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongFile
        fields = '__all__'

