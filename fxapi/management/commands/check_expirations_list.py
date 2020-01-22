from django.core.management.base import BaseCommand
from fxapi.signals import check_expirations_list

class Command(BaseCommand):
    help = 'Check expirations calendar'

    def handle(self, *args, **options):
    	check_expirations_list.send(None)