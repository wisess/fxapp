from django.core.management.base import BaseCommand
from fxapi.signals import load_expirations_calendar

class Command(BaseCommand):
    help = 'Load expirations calendar'

    def handle(self, *args, **options):
    	load_expirations_calendar.send(None)