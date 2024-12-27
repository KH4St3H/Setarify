from django.contrib.auth.models import User
from rest_framework import filters

from api.models import Like


class CustomSearch(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        query_params = request.query_params
        if 'artist' in query_params:
            queryset = queryset.prefetch_related('artist__artists').filter(artist__slug__contains=query_params['artist'])

        if 'album' in query_params:
            queryset = queryset.select_related('album').filter(album__slug=query_params['album'])

        if 'user' in query_params:
            try:
                user = User.objects.get(username=query_params['user'])
            except User.DoesNotExist:
                user = None
            queryset = queryset.filter(id__in=Like.objects.filter(user=user).values_list('song', flat=True))

        return queryset