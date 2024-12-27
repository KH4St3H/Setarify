from rest_framework import permissions
from api.models import Song, Artist, Playlist

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if isinstance(obj, Song):
            return obj.artist.filter(user=request.user).exists()

        if isinstance(obj, Artist):
            return obj.user == request.user

        if isinstance(obj, Song):
            return obj.artist.filter(user=request.user).exists()

        if isinstance(obj, Playlist):
            return obj.author == request.user


class IsArtistOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        return Artist.objects.filter(user=request.user.id).exists()