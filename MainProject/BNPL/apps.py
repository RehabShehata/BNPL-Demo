from django.apps import AppConfig


class BnplConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BNPL'
    def ready(self):
        import BNPL.signals
