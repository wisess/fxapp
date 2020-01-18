import time
import datetime
import re
import os
import requests
from django.dispatch import receiver
from . import signals, services


@receiver(signals.download_expirations_calendar)
def download_expirations_calendar(sender, **kwargs):
	from .parsers import DownloadExpirationsList
	path = '/home/wisess/Study/fxproject/fxapp/tmp/Expirations.csv'

	if(os.path.isfile(path)):
		os.remove(path)
	parser = DownloadExpirationsList()
	parser.download()

	if(os.path.isfile(path)):
		services.print_success('The expirations calendar was downloaded.')
	else:
		services.print_error('Error download the expirations calendar.')
	

@receiver(signals.load_monthly_zones)
def load_monthly_zones(sender, **kwargs):
	services.print_success('Monthly comfort zones data was loaded.')

@receiver(signals.load_weekly_zones)
def load_weekly_zones(sender, **kwargs):
	services.print_success('Weekly comfort zones data was loaded.')

@receiver(signals.load_wednesday_zones)
def load_wednesday_zones(sender, **kwargs):
	services.print_success('Wednesday comfort zones data was loaded.')