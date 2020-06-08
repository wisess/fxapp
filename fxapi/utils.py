def print_success(text: str):
    print("[" + "\033[32m {}".format("OK") + "\033[0m" + " ] " + text)


def print_error(text: str):
    print("[" + "\033[31m {}".format("ERROR") + "\033[0m" + " ] " + text)


def print_notice(text: str):
    print("[" + "\033[33m {}".format("NOTICE") + "\033[0m" + " ] " + text)


def normalize_date(raw_date: str) -> str:
    date_sep = "-"
    date_parts = raw_date.split('/')
    norm_date = date_parts[2] + date_sep + date_parts[0] + date_sep + date_parts[1]
    return norm_date


def get_next_monday_date():
    import datetime

    today_date = datetime.datetime.date(datetime.datetime.today())
    today_weekday = datetime.datetime.isoweekday(datetime.datetime.today())
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


def str_to_numbers(raw_str: str) -> float:
    return max(float(i) for i in raw_str.replace(',', '.').split())


def normalize_symbol_name(raw_name: str) -> str:
    parts_name = raw_name.split("/")
    if len(parts_name) < 2:
        return 'Unknown symbol'
    normalize_name = parts_name[0] + parts_name[1]
    return normalize_name
