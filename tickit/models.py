import uuid
from decimal import Decimal

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name


class Place(models.Model):
    code = models.CharField(max_length=16)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="places")

    class Meta:
        ordering = ["room_id", "code"]
        unique_together = ("code", "room")

    def __str__(self) -> str:
        return f"{self.room.name} - {self.code}"


class Movie(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="sessions")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="sessions")
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        ordering = ["start"]

    def __str__(self) -> str:
        return f"{self.movie.title} ({self.start})"


class TicketStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    SOLD = "sold", "Sold"
    RESERVED = "reserved", "Reserved"


class Ticket(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="tickets")
    place = models.ForeignKey(Place, on_delete=models.PROTECT, related_name="tickets")
    status = models.CharField(
        max_length=16,
        choices=TicketStatus.choices,
        default=TicketStatus.AVAILABLE,
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["session_id", "place_id"]
        unique_together = ("session", "place")

    def __str__(self) -> str:
        return f"Ticket {self.uuid} for {self.session}"
