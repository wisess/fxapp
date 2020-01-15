from django.apps import AppConfig


class FxapiConfig(AppConfig):
    name = 'fxapi'

    def ready(self):
        from . import signals, tasks