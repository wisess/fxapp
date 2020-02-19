def print_success(text):
	print("[" + "\033[32m {}".format("OK")+ "\033[0m" + " ] " + text)

def print_error(text):
	print("[" + "\033[31m {}".format("ERROR")+ "\033[0m" + " ] " + text)

def print_notice(text):
	print("[" + "\033[33m {}".format("NOTICE")+ "\033[0m" + " ] " + text)

def normalize_date(raw_date):
	date_sep = "-"
	date_parts = raw_date.split('/')
	norm_date = date_parts[2]+date_sep+date_parts[0]+date_sep+date_parts[1]
	return norm_date

def get_next_monday_date():
    import time
    import datetime
    
    today_date = datetime.date.today()
    today_weekday = datetime.datetime.isoweekday(today_date)
    next_monday_date = today_date
    if today_weekday == 1:
        next_monday_date = today_date + datetime.timedelta(days=7)
    elif today_weekday == 2:
        next_monday_date = today_date + datetime.timedelta(days=6)
    elif today_weekday == 3:
        next_monday_date = today_date + datetime.timedelta(days=5)
    elif today_weekday == 4:
        next_monday_date = today_date + datetime.timedelta(days=4)
    elif today_weekday == 5:
        next_monday_date = today_date + datetime.timedelta(days=3)
    return next_monday_date

def str_to_numbers(raw_str):
    return max(float(i) for i in raw_str.replace(',','.').split())