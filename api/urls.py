from rest_framework.routers import DefaultRouter

from api.views import PlaylistViewSet, SongViewSet, ArtistViewSet, AlbumViewSet

router = DefaultRouter()
router.register('songs', SongViewSet, basename='song')
router.register('artists', ArtistViewSet, basename='artist')
router.register('albums', AlbumViewSet, basename='album')
router.register('playlists', PlaylistViewSet, basename='playlist')

urlpatterns = router.urls