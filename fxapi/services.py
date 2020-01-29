import time
from datetime import date
from . import models, utils

def get_fx_symbols():
	fx_symbols = models.Symbol.objects.filter(fx_symbol__isnull=False).order_by('symbol')
	return fx_symbols

def get_expiring_contracts(date):
	expiring_contracts = models.Option.objects.filter(expiration=date).order_by('symbol')
	return expiring_contracts

def write_option_contract_to_db(symbol, contract_data):
	option_name = contract_data[0]
	option_type = contract_data[1]
	option_code = contract_data[2]
	option_date = utils.normalize_date(contract_data[3])
	option_instance, created = models.Option.objects.get_or_create(symbol=symbol, option_code=option_code)
	option_instance.symbol = symbol
	option_instance.option_type = option_type
	option_instance.option_code = option_code
	option_instance.expiration = option_date
	option_instance.save()

def write_cab_to_db(option, cab_data):
	# option_name = contract_data[0]
	# option_type = contract_data[1]
	# option_code = contract_data[2]
	# option_date = utils.normalize_date(contract_data[3])
	cab_instance, created = models.ComfortZones.objects.get_or_create(symbol=symbol, option_code=option_code)
	# option_instance.symbol = symbol
	# option_instance.option_type = option_type
	# option_instance.option_code = option_code
	# option_instance.expiration = option_date
	cab_instance.save()