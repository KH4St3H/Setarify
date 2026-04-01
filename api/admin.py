from django.contrib import admin

from api.models import Artist, Like, Song, PlaylistSong, Playlist, Album, SongFile


class SongFileAdmin(admin.ModelAdmin):
    autocomplete_fields = ['song']


class SongAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(Artist)
admin.site.register(Like)
admin.site.register(Song, SongAdmin)
admin.site.register(PlaylistSong)
admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(SongFile, SongFileAdmin)
