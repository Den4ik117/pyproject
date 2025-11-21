from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Place, Session, Ticket, TicketStatus


@receiver(post_save, sender=Session)
def create_tickets_for_session(sender, instance: Session, created: bool, **kwargs) -> None:
    if not created:
        return

    places = Place.objects.filter(room=instance.room)
    tickets = [
        Ticket(session=instance, place=place, status=TicketStatus.AVAILABLE)
        for place in places
    ]
    Ticket.objects.bulk_create(tickets)
