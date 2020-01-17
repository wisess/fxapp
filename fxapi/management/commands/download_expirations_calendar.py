from django.core.management.base import BaseCommand
from fxapi.signals import download_expirations_calendar

class Command(BaseCommand):
    help = 'Download expirations calendar'

    def handle(self, *args, **options):
    	download_expirations_calendar.send(None)