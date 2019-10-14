from django.apps import AppConfig


class TheBrushStashConfig(AppConfig):
    name = 'thebrushstash'

    def ready(self):
        import thebrushstash.signals  # noqa
