from django.contrib import admin
from booking.models import Room, Booking

@admin.display(description='Название комнаты')
def name(obj):
    return obj.name


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (name, 'capacity', 'location')
    search_fields = ('name',)
    empty_value_display = '-пусто-'



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'start_time', 'end_time')
    list_filter = ('room',)
    search_fields = ('user__username',)
