def print_success(text):
	print("[" + "\033[32m {}".format("OK")+ "\033[0m" + " ] " + text)

def print_error(text):
	print("[" + "\033[31m {}".format("ERROR")+ "\033[0m" + " ] " + text)