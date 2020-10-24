from datetime import datetime, time
import csv
import argparse

def check_status(working_time, search_datetime):
    try:
        day = working_time[search_datetime.weekday()]
    except:
        print("Not working today")
        return False
    else:
        # day[0] => opening hours, day[1] => closing hours
        if(search_datetime.time() > day[0] and search_datetime.time() < day[1]):
            return True

    return False


def load_csv(csv_file):
    restaurants_list = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            restaurants_list.append(row)
    restaurants_list.pop(0)

    return restaurants_list

def process_case_4_expression(open_hours_string, days_dict):
    open_hour_tokens = open_hours_string.split("/")
    working_hours = {}

    for open_hour_tokens in open_hour_tokens:
        if("," in open_hour_tokens):
            working_hours.update(process_case_3_expression(open_hour_tokens.strip(), days_dict))
        else: 
            working_hours.update(process_single_expression(open_hour_tokens.strip(), days_dict))

    return working_hours

def process_case_3_expression(open_hours_string, days_dict):
    open_hour_tokens = open_hours_string.split(",")
    days_expression = open_hour_tokens[0]
    days_ints = []
    if("-" in days_expression):
        days_ints = get_working_days(days_expression, days_dict)
    else:
        days_ints.append(days_dict[days_expression.lower()])

    working_time = process_single_expression(open_hour_tokens[1].strip(), days_dict)
    working_hours = list(working_time.values())[0]
    for day in days_ints:
        working_time[day] = working_hours

    return working_time

def process_case_2_expression(open_hours_string, days_dict):
    expression_strings = open_hours_string.split("/")
    working_hours = {}
    for expression_string in expression_strings:
        result = process_single_expression(expression_string.strip(), days_dict)
        working_hours.update(result)

    return working_hours


def get_start_or_finish(expression):
    expression_tokens = expression.split(" ")
    hour_string = expression_tokens[0]
    meridiem = expression_tokens[1]
    minute = None

    if(":" in hour_string):
        time = hour_string.split(":")
        hour = int(time[0])
        minute = int(time[1])
    else:
        hour = int(hour_string)
    
    if("pm" in meridiem):
        hour += 12

    # 0..23 is datetime's hour range, midnight is 00:00 which is not the end of the day, but the start. so 23:59     
    if(hour == 24):
        hour = 23
        minute = 59
    
    minute = minute if minute is not None else 0

    return (hour, minute)

def get_working_hours(hours_expression):
    hours_tokens = hours_expression.split("-")
    from_expression = hours_tokens[0].strip()
    to_expression = hours_tokens[1].strip()
    start_time = get_start_or_finish(from_expression)
    closing_time = get_start_or_finish(to_expression)

    return (start_time, closing_time)


def get_working_days(days_string, days_dict):
    if("-" not in days_string): 
        return [days_dict[days_string.lower()]]

    days_strings = days_string.split("-")
    days_ints = []
    for day in days_strings:
        days_ints.append(days_dict[day.lower()])

    return [*range(days_ints[0], days_ints[1] + 1)]

def process_single_expression(open_hours_string, days_dict):
    days_and_hours_tokens = open_hours_string.split(" ", 1)
    days = days_and_hours_tokens[0]
    working_days = get_working_days(days, days_dict)
    hours_expression = days_and_hours_tokens[1]
    working_hours_tuple = get_working_hours(hours_expression)
    time_opened = {}

    for day in working_days:
        opens = time(hour = working_hours_tuple[0][0], minute = working_hours_tuple[0][1])
        closes = time(hour = working_hours_tuple[1][0], minute = working_hours_tuple[1][1])
        time_opened[day] = (opens, closes)

    return time_opened


days_abbr_lowercase = ["mon", "tues", "wed", "thu", "fri", "sat", "sun"]

def get_days_num_values_dict(days): 
    days_dict = {}
    for i in range(0, len(days)):
        days_dict[days[i]] = i
    return days_dict

"""
Hours column possible formats:
case 1 => Mon-Sun 11:00 am - 10 pm
case 2 => Mon-Thu 11:30 am - 10 pm / Fri-Sun 11:30 am - 11 pm
case 3 => Mon, Wed-Sun 11 am - 10 pm
case 4 => Mon-Thu, Sun 11:30 am - 9 pm / Fri-Sat 11:30 am - 10 pm
"""

def find_open_restaurants(restaurants, search_datetime):
    days_dict = get_days_num_values_dict(days_abbr_lowercase)
    
    opened = []
    working_time = None

    for restaurant in restaurants:
        open_hours_string = restaurant[1]

        if("," in open_hours_string and "/" in open_hours_string):
            working_time = process_case_4_expression(open_hours_string, days_dict)
        elif("," in open_hours_string and "/" not in open_hours_string):
            working_time = process_case_3_expression(open_hours_string, days_dict)
        elif("/" in open_hours_string and "," not in open_hours_string):
            working_time = process_case_2_expression(open_hours_string, days_dict)
        elif("/" not in open_hours_string and "," not in open_hours_string):
            working_time = process_single_expression(open_hours_string, days_dict)

        if(working_time is not None):
            is_open = check_status(working_time, search_datetime)
            if(is_open):
                opened.append(f"{restaurant[0]}, working hours: {restaurant[1]}")

    print(f"Working at {search_datetime}:")
    for info_str in opened:
        print(info_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser() 
    default_csv_file = "restaurants.csv"
    default_search_datetime = datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M')

    parser.add_argument("-csv_file", type=str, default=default_csv_file, action="store", dest="csv_file")
    parser.add_argument("-search_datetime", type=str, default=default_search_datetime, action="store", dest="search_datetime")
    args = parser.parse_args()

    restaurants = load_csv(args.csv_file)

    search_datetime = datetime.strptime(args.search_datetime, '%Y-%m-%d %H:%M')

    find_open_restaurants(restaurants, search_datetime)