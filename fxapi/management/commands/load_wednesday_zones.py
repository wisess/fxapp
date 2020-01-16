from django.core.management.base import BaseCommand
from fxapi.signals import load_wednesday_zones

class Command(BaseCommand):
    help = 'Load wednesday comfort zones data'

    def handle(self, *args, **options):
    	load_wednesday_zones.send(None)