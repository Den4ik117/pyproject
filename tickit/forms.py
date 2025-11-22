from django import forms

from .models import Movie, Place, Session


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "description", "duration"]
        labels = {
            "title": "Название",
            "description": "Описание",
            "duration": "Длительность (мин)",
        }

    def clean_duration(self):
        duration = self.cleaned_data["duration"]
        if duration <= 0:
            raise forms.ValidationError("Длительность должна быть больше нуля.")
        return duration


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ["movie", "room", "start", "end"]
        labels = {
            "movie": "Фильм",
            "room": "Зал",
            "start": "Начало сеанса",
            "end": "Окончание сеанса",
        }
        widgets = {
            "start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dt_format = "%Y-%m-%dT%H:%M"
        self.fields["start"].input_formats = [dt_format]
        self.fields["end"].input_formats = [dt_format]
        self.fields["start"].widget.format = dt_format
        self.fields["end"].widget.format = dt_format

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        movie = cleaned_data.get("movie")

        if start and end and start >= end:
            self.add_error("end", "Окончание должно быть позже начала.")

        if start and end and movie:
            duration_minutes = (end - start).total_seconds() / 60
            if duration_minutes < movie.duration:
                self.add_error(
                    "end",
                    "Промежуток между началом и окончанием меньше длительности фильма.",
                )

        return cleaned_data


class TicketPurchaseForm(forms.Form):
    ACTION_RESERVE = "reserve"
    ACTION_BUY = "buy"

    ACTION_CHOICES = (
        (ACTION_RESERVE, "Забронировать"),
        (ACTION_BUY, "Купить"),
    )

    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        label="Сеанс",
        empty_label="Выберите сеанс",
    )
    place = forms.ModelChoiceField(
        queryset=Place.objects.none(),
        label="Место",
        empty_label="Выберите место",
    )
    action = forms.ChoiceField(
        choices=ACTION_CHOICES, label="Действие", widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        session_id = kwargs.pop("session_id", None)
        super().__init__(*args, **kwargs)

        effective_session_id = (
            session_id
            or self.data.get("session")
            or self.initial.get("session")
        )

        if effective_session_id:
            try:
                session = Session.objects.get(pk=effective_session_id)
            except Session.DoesNotExist:
                return

            self.fields["place"].queryset = session.room.places.all()
            self.initial.setdefault("session", session)

    def clean_place(self):
        place = self.cleaned_data["place"]
        session = self.cleaned_data.get("session")

        if session and place.room_id != session.room_id:
            raise forms.ValidationError("Это место не относится к выбранному залу.")

        return place
