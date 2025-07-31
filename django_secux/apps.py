from django.apps import AppConfig

class DjangoSecuxConfig(AppConfig):
    name = 'django_secux'
    verbose_name = 'Django Secux'

    def ready(self):
        from . import signals
