from django.db.models import F, Case, When, Value, BooleanField
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from api.filters import CustomSearch
from api.models import Playlist, Song, Artist, Album, PlaylistSong, Like
from api.permissions import IsOwnerOrReadOnly, IsArtistOrReadOnly
from api.serializers import ArtistSerializer, AlbumSerializer, SongSerializer, PlaylistSerializer, \
    AlbumWithSongsSerializer, PlaylistWithSongsSerializer, PlaylistSongSerializer, SongFileUrlSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = Playlist.objects.all()
    serializer_class = PlaylistWithSongsSerializer

    lookup_field = 'slug'

    @extend_schema(request=PlaylistSongSerializer, responses=PlaylistSongSerializer)
    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrReadOnly])
    def add_song(self, request, slug=None):
        playlist = self.get_object()
        serializer = PlaylistSongSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        song = serializer.validated_data.pop('song_slug')

        if PlaylistSong.objects.filter(playlist=playlist, song=song.id).exists():
            return Response({'error': 'Song already exists in this album'}, status=status.HTTP_400_BAD_REQUEST)

        playlist.songs.filter(order__gte=request.data['order']).update(order=F('order') + 1)
        serializer.validated_data['order'] = min(playlist.songs.count() + 1, serializer.validated_data['order'])
        serializer.validated_data['playlist'] = playlist
        serializer.validated_data['song'] = song
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter('song_slug', OpenApiTypes.STR)
        ]
    )
    @action(detail=True, methods=['delete'], permission_classes=[IsOwnerOrReadOnly])
    def delete_song(self, request, slug=None):
        playlist = self.get_object()
        song_slug = request.query_params.get('song_slug', '')
        try:
            song = Song.objects.get(slug=song_slug)
        except Song.DoesNotExist:
            return Response({'error': 'Song does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ps = PlaylistSong.objects.get(song=song, playlist=playlist)
        except PlaylistSong.DoesNotExist:
            return Response({'error': 'Song does not exist in Playlist'}, status=status.HTTP_400_BAD_REQUEST)

        order = ps.order
        ps.delete()
        playlist.songs.filter(order__gt=order).update(order=F('order') - 1)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == 'list':
            return PlaylistSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.author = self.request.user
        obj.save()


class SongViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsArtistOrReadOnly]
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    lookup_field = 'slug'
    ordering = ['created_at']

    filter_backends = [filters.SearchFilter, CustomSearch]
    search_fields = ['title', 'artist__name', 'genre']

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_authenticated:
            return queryset.annotate(
                liked=Case(
                    When(
                        likes__user=self.request.user, then=Value(True)
                    ),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter('artist', OpenApiTypes.STR, description='slug for requested artist', required=False),
            OpenApiParameter('album', OpenApiTypes.STR, description='slug for requested album', required=False),
            OpenApiParameter('user', OpenApiTypes.STR, description='slug for requested user', required=False),
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(responses=SongFileUrlSerializer)
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_url(self, request, slug=None):
        song = self.get_object()
        song.hit_count += 1
        song.save()
        serializer = SongFileUrlSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def like(self, request, slug=None):
        song = self.get_object()
        like, created = Like.objects.get_or_create(song=song, user=request.user)
        if created:
            song.like_count += 1
            song.save()
        return Response(None, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def dislike(self, request, slug=None):
        song = self.get_object()
        try:
            like = Like.objects.get(song=song, user=request.user)
        except Like.DoesNotExist:
            return Response(None, status=status.HTTP_200_OK)
        like.delete()
        song.like_count -= 1
        song.save()
        return Response(None, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.artist.add(self.request.user.artist)
        obj.save()


class ArtistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    lookup_field = 'slug'


class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsArtistOrReadOnly]
    queryset = Album.objects.all().prefetch_related('songs').prefetch_related('artist')
    serializer_class = AlbumSerializer

    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AlbumWithSongsSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.artist.add(self.request.user.artist)
        obj.save()
