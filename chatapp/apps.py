from django.apps import AppConfig
import sys
from django.http import HttpResponse


class ChatappConfig(AppConfig):
    name = 'chatapp'
    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        # you must import your modules here
        # to avoid AppRegistryNotReady exception








