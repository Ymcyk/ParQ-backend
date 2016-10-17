from django.apps import AppConfig


class BadgesConfig(AppConfig):
    name = 'badges'

    def ready(self):
        import badges.signals
