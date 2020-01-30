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
	start_date = date.today()
	if option.option_type == 'Friday':
		start_date = utils.get_next_monday_date()
	curr_contracts = models.Option.objects.filter(symbol=option.symbol).filter(option_type=option.option_type).filter(expiration__gte=option.expiration).order_by('expiration')
	cab_instance, created = models.ComfortZones.objects.get_or_create(symbol=option.symbol, option_code=option.option_code)
	cab_instance.symbol 		= option.symbol
	cab_instance.fx_symbol 		= option.symbol.fx_symbol
	cab_instance.option_code 	= option.option_code
	cab_instance.zone_type 		= option.option_type
	cab_instance.start_date 	= start_date
	cab_instance.end_date 		= curr_contracts[1].expiration
	cab_instance.call_strike 	= cab_data['call_strike']
	cab_instance.balance 		= cab_data['balance']
	cab_instance.put_strike 	= cab_data['put_strike']
	cab_instance.save()