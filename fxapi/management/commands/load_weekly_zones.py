from django.core.management.base import BaseCommand
from fxapi.signals import load_weekly_zones

class Command(BaseCommand):
    help = 'Load weekly comfort zones data'

    def handle(self, *args, **options):
    	load_weekly_zones.send(None)