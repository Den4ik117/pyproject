from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MovieForm, SessionForm, TicketPurchaseForm
from .models import Session, Ticket, TicketStatus


def home(request):
    return render(request, "tickit/index.html")


def create_movie(request):
    form = MovieForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        movie = form.save()
        messages.success(request, f"Фильм «{movie.title}» создан.")
        return redirect("session_create")

    return render(request, "tickit/movie_form.html", {"form": form})


def create_session(request):
    form = SessionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        session = form.save()
        messages.success(
            request,
            "Расписание создано, билеты для всех мест отмечены как свободные.",
        )
        return redirect("ticket_purchase")

    return render(request, "tickit/session_form.html", {"form": form})


def ticket_purchase(request):
    session_id = request.GET.get("session") or request.POST.get("session")
    form = TicketPurchaseForm(request.POST or None, session_id=session_id)

    selected_session = None
    tickets = []
    if session_id:
        selected_session = Session.objects.filter(pk=session_id).first()
        if selected_session:
            tickets = (
                Ticket.objects.filter(session=selected_session)
                .select_related("place")
                .order_by("place__code")
            )

    if request.method == "POST" and form.is_valid():
        session = form.cleaned_data["session"]
        place = form.cleaned_data["place"]
        action = form.cleaned_data["action"]

        with transaction.atomic():
            ticket = (
                Ticket.objects.select_for_update()
                .filter(session=session, place=place)
                .first()
            )
            if not ticket:
                form.add_error(None, "Билет для этого места не найден.")
            elif ticket.status != TicketStatus.AVAILABLE:
                form.add_error(None, "Место уже занято.")
            else:
                ticket.status = (
                    TicketStatus.SOLD
                    if action == TicketPurchaseForm.ACTION_BUY
                    else TicketStatus.RESERVED
                )
                ticket.save()
                messages.success(request, "Операция выполнена.")
                return redirect("ticket_detail", uuid=str(ticket.uuid))

    context = {
        "form": form,
        "selected_session": selected_session,
        "tickets": tickets,
    }
    return render(request, "tickit/ticket_purchase.html", context)


def ticket_detail(request, uuid):
    ticket = get_object_or_404(
        Ticket.objects.select_related("session__movie", "session__room", "place"),
        uuid=uuid,
    )
    return render(request, "tickit/ticket_detail.html", {"ticket": ticket})
