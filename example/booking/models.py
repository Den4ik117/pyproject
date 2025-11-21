from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


User = settings.AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return f'{self.name} (вместимость {self.capacity})'


class Booking(models.Model):
    room = models.ForeignKey('Room', on_delete=models.PROTECT, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """https://docs.djangoproject.com/en/5.2/ref/models/options/"""
        ordering = ['start_time']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                    name='end_after_start_time'),
        ]
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'{self.room.name} - {self.start_time} - {self.end_time}'

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError('end_time должно быть больше start_time')

        from django.utils import timezone

        start = timezone.make_aware(self.start_time) if timezone.is_naive(self.start_time) else self.start_time
        end = timezone.make_aware(self.end_time) if timezone.is_naive(self.end_time) else self.end_time

        overlapping = Booking.objects.filter(
            room=self.room,
            start_time__lte=end,
            end_time__gt=start,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError(
                'Это время уже занято для этой комнаты'
            )
