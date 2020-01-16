from django.core.management.base import BaseCommand
from fxapi.signals import load_monthly_zones

class Command(BaseCommand):
    help = 'Load monthly comfort zones data'

    def handle(self, *args, **options):
    	load_monthly_zones.send(None)