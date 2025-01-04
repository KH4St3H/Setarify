from django.contrib import admin

from api.models import Artist, Like, Song, PlaylistSong, Playlist, Album, SongFile

admin.site.register(Artist)
admin.site.register(Like)
admin.site.register(Song)
admin.site.register(PlaylistSong)
admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(SongFile)
