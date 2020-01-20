from django.core.management.base import BaseCommand
from fxapi.signals import pars_expirations_calendar

class Command(BaseCommand):
    help = 'Pars expirations calendar'

    def handle(self, *args, **options):
    	pars_expirations_calendar.send(None)