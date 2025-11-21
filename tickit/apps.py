from django.apps import AppConfig


class TickitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickit'

    def ready(self) -> None:
        # Import signal handlers to auto-create tickets on session creation.
        from . import signals  # noqa: F401
