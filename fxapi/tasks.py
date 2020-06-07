import os
from datetime import date

from django.dispatch import receiver

from . import services, signals, utils

EXP_LIST_FILE_PATH = os.getenv("EXPIRATIONS_LIST_FILE_PATH")


@receiver(signals.download_expirations_calendar)
def download_expirations_calendar(sender, **kwargs):
    from .parsers import DownloadExpirationsList

    if os.path.isfile(EXP_LIST_FILE_PATH):
        os.remove(EXP_LIST_FILE_PATH)
    parser = DownloadExpirationsList()
    parser.open()
    parser.download()
    parser.close()

    if os.path.isfile(EXP_LIST_FILE_PATH):
        utils.print_success('The expirations calendar was downloaded.')
    else:
        utils.print_error('Error download the expirations calendar.')


@receiver(signals.pars_expirations_calendar)
def pars_expirations_calendar(sender, **kwargs):
    from .parsers import ParseExpirationsList
    if os.path.isfile(EXP_LIST_FILE_PATH):
        parser = ParseExpirationsList()
        contracts = parser.parse()
        symbols = services.get_fx_symbols()
        for symbol in symbols:
            for contract in contracts:
                option_name = contract[0]
                if option_name == symbol.symbol:
                    services.write_option_contract_to_db(symbol, contract)
        utils.print_success("Expirations list file was parsed.")
    else:
        utils.print_error("Expirations list file doesn\'t exist.")


@receiver(signals.check_expirations_list)
def check_expirations_list(sender, **kwargs):
    from .parsers import ParseSettleDataFromCme
    today = date.today()
    contracts_list = services.get_expiring_contracts(today)
    if len(contracts_list) > 0:
        cab_count = 0
        for contract in contracts_list:
            parser = ParseSettleDataFromCme(contract)
            parser.open()
            cab_data = parser.parse()
            parser.close()
            if cab_data != 0:
                services.write_cab_to_db(contract, cab_data)
                cab_count = cab_count + 1
        if cab_count != 0:
            utils.print_success("Comfort zones were write successfully for {} symbols".format(cab_count))
    else:
        utils.print_notice("No expiring contracts.")
