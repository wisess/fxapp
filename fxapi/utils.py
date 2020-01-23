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