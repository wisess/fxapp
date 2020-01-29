import time
from datetime import date
import re
import os
import requests
from django.dispatch import receiver
from . import services, signals, utils

EXP_LIST_FILE_PATH = os.getenv("EXPIRATIONS_LIST_FILE_PATH")

@receiver(signals.download_expirations_calendar)
def download_expirations_calendar(sender, **kwargs):
	from .parsers import DownloadExpirationsList
	

	if(os.path.isfile(EXP_LIST_FILE_PATH)):
		os.remove(EXP_LIST_FILE_PATH)
	parser = DownloadExpirationsList()
	parser.download()

	if(os.path.isfile(EXP_LIST_FILE_PATH)):
		utils.print_success('The expirations calendar was downloaded.')
	else:
		utils.print_error('Error download the expirations calendar.')

@receiver(signals.pars_expirations_calendar)
def pars_expirations_calendar(sender, **kwargs):
	from .parsers import ParseExpirationsList
	if(os.path.isfile(EXP_LIST_FILE_PATH)):
		parser = ParseExpirationsList()
		contracts = parser.parse()
		symbols = services.get_fx_symbols()
		for symbol in symbols:
			for contract in contracts:
				option_name = contract[0]
				if option_name==symbol.symbol:
					services.write_option_contract_to_db(symbol, contract)
		utils.print_success("Expirations list file was parsed.")
	else:
		utils.print_error("Expirations list file doesn\'t exist.")

@receiver(signals.check_expirations_list)
def check_expirations_list(sender, **kwargs):
	from .parsers import ParseSettleDataFromCme
	today = date.today()
	contracts_list = services.get_expiring_contracts(today)
	if len(contracts_list)>0:
		for contract in contracts_list:
			parser = ParseSettleDataFromCme(contract)
			cab_data = parser.parse()
	else:
		utils.print_notice("No expiring contracts.")

@receiver(signals.load_monthly_zones)
def load_monthly_zones(sender, **kwargs):
	utils.print_success('Monthly comfort zones data was loaded.')

@receiver(signals.load_weekly_zones)
def load_weekly_zones(sender, **kwargs):
	utils.print_success('Weekly comfort zones data was loaded.')

@receiver(signals.load_wednesday_zones)
def load_wednesday_zones(sender, **kwargs):
	utils.print_success('Wednesday comfort zones data was loaded.')