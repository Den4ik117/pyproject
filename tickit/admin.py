from django.contrib import admin

from .models import Movie, Place, Room, Session, Ticket


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "room")
    list_filter = ("room",)
    search_fields = ("code",)
    list_select_related = ("room",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "duration")
    search_fields = ("title",)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "room", "start", "end")
    list_filter = ("room", "movie")
    search_fields = ("movie__title",)
    list_select_related = ("movie", "room")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("uuid", "session", "place", "status", "price")
    list_filter = ("status", "session__movie", "session__room")
    search_fields = ("uuid", "session__movie__title", "place__code")
    list_select_related = ("session", "place", "session__movie", "session__room")
