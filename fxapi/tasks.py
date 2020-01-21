import time
import datetime
import re
import os
import requests
from django.dispatch import receiver
from . import signals, services

EXP_LIST_FILE_PATH = os.getenv("EXPIRATIONS_LIST_FILE_PATH")

@receiver(signals.download_expirations_calendar)
def download_expirations_calendar(sender, **kwargs):
	from .parsers import DownloadExpirationsList
	

	if(os.path.isfile(EXP_LIST_FILE_PATH)):
		os.remove(EXP_LIST_FILE_PATH)
	parser = DownloadExpirationsList()
	parser.download()

	if(os.path.isfile(EXP_LIST_FILE_PATH)):
		services.print_success('The expirations calendar was downloaded.')
	else:
		services.print_error('Error download the expirations calendar.')

@receiver(signals.pars_expirations_calendar)
def pars_expirations_calendar(sender, **kwargs):
	from .parsers import ParseExpirationsList
	if(os.path.isfile(EXP_LIST_FILE_PATH)):
		parser = ParseExpirationsList()
		contracts = parser.parse()
		print(contracts)
	else:
		services.print_error("Expirations list file doesn\'t exist.")

@receiver(signals.load_monthly_zones)
def load_monthly_zones(sender, **kwargs):
	services.print_success('Monthly comfort zones data was loaded.')

@receiver(signals.load_weekly_zones)
def load_weekly_zones(sender, **kwargs):
	services.print_success('Weekly comfort zones data was loaded.')

@receiver(signals.load_wednesday_zones)
def load_wednesday_zones(sender, **kwargs):
	services.print_success('Wednesday comfort zones data was loaded.')