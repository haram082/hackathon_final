import codecs
import chardet
import csv
import os
import sys


with open('text_file.txt', 'rb') as f:
    result_encoding = chardet.detect(f.read())

print(result_encoding['encoding'])

with codecs.open('text_file.txt', 'r', encoding='Windows-1252') as f:
    content = f.read()

with codecs.open('text_file.txt', 'w', encoding='utf-8') as f:
    f.write(content)

def parse_text(text_file, class_name = "", export_file = "export.csv"):
    """
    searches for keywords, key times/dates, key locations

    :param text_file: (txt file)
    :return: csv file
    """
    in_text = open(text_file, "r", encoding="utf8")
    text_list = list(in_text)
    text_list_edit = clear_empty_lines(text_list)
    # in text without empty lines
    lines = list(enumerate(text_list_edit))

    lines_lower = []
    for pair in lines:
        lines_lower.append((pair[0], pair[1].lower()))

    all_events = []

    office_hours_keywords = ["office hour"]
    mentor_session_keywords = ["mentor"]
    class_times_keywords = ["lecture, class time"]

    if search_line(lines_lower, office_hours_keywords, "Office Hours"):
        all_events.append(search_line(lines_lower, office_hours_keywords, class_name + " Office Hours"))

    if search_line(lines_lower, mentor_session_keywords, "Mentor Sessions"):
        all_events.append(search_line(lines_lower, mentor_session_keywords, class_name + " Mentor Sessions"))

    if search_line(lines_lower, class_times_keywords, "Class Times"):
        all_events.append(search_line(lines_lower, class_times_keywords, class_name + " Class Times"))

    print(export_format(all_events), export_file)
    write_csv(export_format(all_events), export_file)

    in_text.close()

def find_time(lines_index, lines_lower):
    """

    :param lines_index:
    :param lines_lower:
    :return:
    """
    line = lines_lower[lines_index][1] + " " + lines_lower[lines_index + 1][1]
    line = line.replace(",", " ").replace("-", " ").replace("(", " ").replace(")", " ").replace(";", " ")
    line = line.replace(" am", "am").replace(" pm", "pm")
    line_list = line.split(" ")
    while "" in line_list:
        line_list.remove("")

    fix_dates(line_list)
    fix_times(line_list)
    return (line_list)


def fix_times(time_list):

    for i in range(len(time_list) - 1, -1, -1):
        time_list[i].replace(".", ":")
        if time_list[i][0].isdigit():
            if ":" not in time_list[i] and "am" not in time_list[i] and "pm" not in time_list[i]:
                if time_list[i].isdigit():
                    if int(time_list[i]) >= 13:
                        time_list.pop(i)
                else:
                    time_list.pop(i)


def search_line(lines_lower, keywords, name):

    office_hours_return = []
    for keyword in keywords:
        for pair in lines_lower:
            line = pair[1]

            if keyword in line:
                office_hours = find_time(pair[0], lines_lower)
                if office_hours:
                    office_hours_return = convert(office_hours, name)
                    break

    return office_hours_return

def fix_dates(time_list):

    date_dict = create_date_dict()
    for i in range(len(time_list) - 1, -1, -1):
        if not time_list[i][0].isdigit() and not time_list[i] in date_dict:
            time_list.pop(i)

        elif time_list[i] in date_dict:
            time_list[i] = date_dict[time_list[i]]


def create_date_dict():

    return_dict = {"monday": "m", "tuesday": "t", "wednesday": "w", "thursday": "r", "friday": "f", "mon": "m",
                   "tue": "t", "wed": "w", "thu": "r", "fri": "f", "am": "am", "pm": "pm"}

    days_of_week = ["m", "t", "w", "r", "f"]
    for i in range(len(days_of_week)):
        return_dict[days_of_week[i]] = days_of_week[i]
        j_list = days_of_week[i+1:]
        for j in range(len(j_list)):
            return_dict[days_of_week[i] + j_list[j]] = days_of_week[i] + j_list[j]
            k_list = j_list[j + 1:]
            for k in range(len(k_list)):
                return_dict[days_of_week[i] + j_list[j] + k_list[k]] = days_of_week[i] + j_list[j] + k_list[k]
                l_list = k_list[k + 1:]
                for l in range(len(l_list)):
                    return_dict[days_of_week[i] + j_list[j] + k_list[k] + l_list[l]] = days_of_week[i] + j_list[j] + k_list[k] + l_list[l]

    return return_dict

def convert(list, keyword):
    if len(list) <= 2:
        return []

    events = [[]]
    is_digit = False
    was_digit = False
    was_was_digit = False

    for elem in list:
        if len(events[-1]) == 3:
            events.append([])
        if elem[0].isdigit():
            is_digit = True
            if not was_digit or not was_was_digit:
                events[-1].append(elem.replace(".",":"))

        else:
            events[-1].insert(0, elem)
            is_digit = False

        was_was_digit = was_digit
        was_digit = is_digit
        # updates was_digit and was_was_digit

    events.insert(0, keyword)
    if len(events[-1]) != 3:
        events.pop(-1)

    return events

def export_format(all_events):
    """

    :param all_events: (list) in format [[name, [days, start time, end time]...]
    :return:
    """
    return_list = []
    days_dict = {"m": 4, "t": 5, "w": 6, "r": 0, "f": 1}
    for event in all_events:
        for day in event[1][0]:
            num = 18 + days_dict[day]
            while num <= 132:
                return_list.append([event[0], date_format(num) + event[1][1], date_format(num) + event[1][2]])
                num += 7

    return return_list

def date_format(date_num):
    """
    export date in form month/day/23
    :param date_num:
    :return:
    """
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    index = 0
    while date_num > month_lengths[index]:
        date_num -= month_lengths[index]
        index += 1

    return str(index + 1) + "/" + str(date_num) + "/23 "


def write_csv(export_list, file_name = "export.csv"):
    with open(file_name, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        for event in export_list:
            writer.writerow(event)

def clear_empty_lines(lines):
    """

    :param lines:
    :return:
    """
    return_lines = []
    for line in lines:
        if line.rstrip("\n") != "":
            return_lines.append(line.rstrip("\n"))

    return return_lines


parse_text("text_file.txt", "Economic Statistics", "export.csv")
