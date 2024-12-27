from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Playlist, Song, Artist, Album
from api.permissions import IsOwnerOrReadOnly, IsArtistOrReadOnly
from api.serializers import ArtistSerializer, AlbumSerializer, SongSerializer, PlaylistSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class SongViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsArtistOrReadOnly]
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsArtistOrReadOnly]
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
