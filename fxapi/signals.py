from django.dispatch import Signal

download_expirations_calendar	= Signal()
pars_expirations_calendar		= Signal()
check_expirations_list			= Signal()
load_monthly_zones				= Signal()
load_weekly_zones				= Signal()
load_wednesday_zones			= Signal()