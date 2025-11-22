from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/new/", views.create_movie, name="movie_create"),
    path("sessions/new/", views.create_session, name="session_create"),
    path("tickets/purchase/", views.ticket_purchase, name="ticket_purchase"),
    path("tickets/<uuid:uuid>/", views.ticket_detail, name="ticket_detail"),
]
