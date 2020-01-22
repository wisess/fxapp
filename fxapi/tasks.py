import time
import datetime
import re
import os
import requests
from django.dispatch import receiver
from . import models, signals, services

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
		symbols = models.Symbol.objects.filter(cme_pid__isnull=False).order_by('symbol')
		for symbol in symbols:
			for contract in contracts:
				option_name = contract[0]
				option_type = contract[1]
				option_code = contract[2]
				option_date = services.normalize_date(contract[3])
				if option_name==symbol.symbol:
					option_instance, created = models.Option.objects.get_or_create(symbol=symbol, option_code=option_code)
					option_instance.symbol = symbol
					option_instance.option_type = option_type
					option_instance.option_code = option_code
					option_instance.expiration = option_date
					option_instance.save()
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